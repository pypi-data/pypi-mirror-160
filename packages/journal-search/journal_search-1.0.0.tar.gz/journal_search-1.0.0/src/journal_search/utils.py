import csv
import re
import time
import traceback
from typing import List
import pandas as pd
import playwright
from icecream import ic
from loguru import logger
from parsel import Selector
from playwright.async_api import async_playwright
from tenacity import retry, stop_after_attempt
from pathlib import Path
baseurl = "https://www.letpub.com.cn/"
ccf_path = str(Path(__file__).parent / "data" / "CCF2019.csv")

def ccf_filter(category: List[str], level: List[str], domain: List[str], publisher: List[str]):
    """根据给定条件在CCF推荐列表中筛选出符合条件的条目
    Args:
        category(List[str]): 推荐类型列表
        level(List[str]): 推荐等级列表
        domain(List[str]): 学科领域列表
        publisher(List[str]): 出版社列表
    """
    try:
        df = pd.read_csv(ccf_path)
        mapping = {
            'category': {
                "journal": "推荐国际学术刊物",
                "cn_journal": "推荐中文科技期刊",
                "conference": "推荐国际学术会议",
            },
            'level': {
                "A": "A类",
                "B": "B类",
                "C": "C类",
            },
            'domain': {
                "1": "人工智能",
                "2": "计算机体系结构/并行与分布计算/存储系统",
                "3": "软件工程/系统软件/程序设计语言",
                "4": "数据库/数据挖掘/内容检索",
                "5": "网络与信息安全",
                "6": "计算机图形学与多媒体",
                "7": "计算机网络",
                "8": "计算机科学理论",
                "9": "交叉/综合/新兴",
                "10": "人机交互与普适计算",
            },
            'publisher': {
                "Springer": "Springer",
                "IEEE": "IEEE",
                "ACM": "ACM",
                "Elsevier": "Elsevier",
            },
        }
        # 类型筛选
        df_list = []
        for i in category:
            t_df = df[df["category"]==mapping['category'][i]]
            df_list.append(t_df)
        df = pd.concat(df_list)
        # 等级筛选
        df_list = []
        for i in level:
            t_df = df[df["level"]==mapping['level'][i]]
            df_list.append(t_df)
        df = pd.concat(df_list)
        # 学科筛选
        df_list = []
        for i in domain:
            if i != '0':
                t_df = df[df["domain"]==mapping['domain'][i]]
            else:
                t_df = df[df['domain'].isna()]
            df_list.append(t_df)
        df = pd.concat(df_list)
        # 出版社筛选
        df_list = []
        for i in publisher:
            if i != 'other':
                t_df = df[df["publisher"]==mapping['publisher'][i]]
            else:
                t_df = df[~df["publisher"].isin(['Springer', 'IEEE', 'ACM', 'Elsevier'])]
            df_list.append(t_df)
        df = pd.concat(df_list)
        logger.success(f"筛选出{len(df)}条记录!")
        out = []
        if len(df) > 0:
            df['abbr'] = df["abbr"].fillna("无")
            df['publisher'] = df["publisher"].fillna("/")
            df['domain'] = df["domain"].fillna("/")
            i = 1
            for j, item in df.iterrows():
                row = {
                    "name": item['name'],
                    "abbr": item['abbr'],
                    "publisher": item['publisher'],
                    "domain": item['domain'],
                    "ccf_category": item['category'],
                    "ccf_level": item['level'],
                    "website": item['website'],
                    "key": i,
                }
                i += 1
                out.append(row)
        return out
    except:
        logger.error(traceback.format_exc())

def isConference(name: str) -> bool:
    """判断给定的名称是否为会议
    Args:
        name(str): 期刊/会议 名称
    """
    m = re.search("([12]\d{3})", name)
    if m is not None:
        return True
    conference_keywords = ['Conference', 'Symposium', 'Workshop', 'Proceeding']
    for keyword in conference_keywords:
        if keyword.lower() in name.lower():
            return True
    return False

def searchInCCF(keyword: str):
    """在CCF推荐列表中搜索关键词keyword
    Args:
        keyword(str): 搜索的关键词
    """
    try:
        df = pd.read_csv(ccf_path)
        parts = keyword.split()

        # 去除开头/结尾年份
        if re.match("\d{4}", parts[0]):
            del parts[0]
        if re.match("\d{4}", parts[-1]):
            del parts[-1]

        keyword = " ".join(parts)
        df['temp_name'] = df['name'].str.upper()
        res1 = df[df['temp_name'].str.contains(keyword.upper(), regex=False)]
        res2 = df[df['abbr'].str.upper()==keyword.upper()]
        res = pd.concat([res1, res2])
        res = res.drop_duplicates()
        out = []
        if len(res)>0:
            res['abbr'] = res['abbr'].fillna("无")
            res['domain'] = res['domain'].fillna("/")
            i = 1
            for j, item in res.iterrows():
                row = {
                    "name": item['name'],
                    "abbr": item['abbr'],
                    "publisher": item['publisher'],
                    "domain": item['domain'],
                    "ccf_category": item['category'],
                    "ccf_level": item['level'],
                    "website": item['website'],
                    "key": i,
                    "note": '',
                    "state": "找到",
                }
                i+=1
                out.append(row)
        else:
            out.append({
                "key": 1,
                "name": keyword,
                "note": "未找到！",
                "state": "未找到",
            })
        return out
    except:
        logger.error(f"error for handling '{keyword}'")
        logger.error(traceback.format_exc())

def searchInCCFBatch(keyword_list: List[str]):
    """在CCF推荐列表中批量搜索关键词列表keyword_list
    Args:
        keyword_list(List[str]): 待搜索的关键词列表
    """
    result = []
    for i, keyword in enumerate(keyword_list):
        out = searchInCCF(keyword)
        if out is not None:
            row = out[0]
            row['key'] = i+1
            if len(out) > 1:
                row['note'] = f"关键词“{keyword}”找到多条记录"
            result.append(row)
    return result

@retry(stop=stop_after_attempt(5))
async def searchInLetpub(keyword: str, headless: bool = False):
    """在Letpub网站中搜索关键词keyword
    Args:
        keyword(str): 待搜索的关键词
        headless(bool): 是否以无头模式运行
    """
    async with async_playwright() as p:
        url = "https://www.letpub.com.cn/index.php?page=journalapp&view=search"
        try:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)
            await page.reload()
            # await page.click("#layui-layer1 > span.layui-layer-setwin > a")
            await page.fill("#searchname", keyword)
            await page.click("#yxyz_content > form > table > tbody > tr:nth-child(1) > td:nth-child(6) > input[type=submit]:nth-child(2)")
            # time.sleep(3)
            result = await page.evaluate('delete layer')
            # print(result)
            result = await page.locator("#yxyz_content > b").inner_text()
            count = eval(re.search("(\d+)", result).groups()[0])
            if count >= 1:
                logger.info(f"'{keyword}' 匹配到{count}条记录!")
                link = await page.locator("#yxyz_content > table.table_yjfx > tbody > tr:nth-child(4) > td:nth-child(2) > a").get_attribute("href")
                detail_url = f"{baseurl}{link[2:]}"
                await page.goto(detail_url)
                while True:
                    content = await page.content()
                    row = parse(content)
                    ic("first", row)
                    if not row: # 解析失败
                        time.sleep(1)
                        await page.reload()
                        continue
                    row['详情'] = detail_url
                    row['key'] = 1
                    if count>1:
                        row['备注'] = f"letpub匹配到{count}条记录，请人工核对！"
                        row['state'] = "找到(多条)"
                    else:
                        row['state'] = "找到(唯一)"
                    return [row]
            else:
                logger.warning(f"'{keyword}' 匹配到{count}条记录!")
                row = {
                    "期刊名字": keyword,
                    "备注": f"letpub匹配到{count}条记录",
                    "state": "未找到",
                    "key": 1,
                }
                return [row]
        except playwright._impl._api_types.TimeoutError:
            logger.error("超时错误!")
            raise Exception("Timeout Error")
        except:
            logger.error(traceback.format_exc())
            raise Exception("Error")

def parse(content: str):
    """解析并提取Letpub网页期刊信息
    Args:
        content(str): 网页html文件内容
    """
    selector = Selector(content)
    tbody_selector = selector.css("#yxyz_content > table:nth-child(12) > tbody")
    result = {}
    roi_fields = ["期刊名字", "期刊ISSN", "h-index", "期刊官方网站", "是否OA开放访问", "出版商", "涉及的研究方向", "出版国家或地区", "出版语言", "出版周期", "出版年份", "WOS期刊SCI分区", "中科院SCI期刊分区", "平均审稿速度", "平均录用比例"]
    cas_first = True
    for tr in tbody_selector.css("tr")[1:]:
        field_name = str(tr.css("tr > td:nth-child(1)::text").get()).strip()
        if field_name in roi_fields:
            if field_name in ["期刊ISSN", "h-index", "是否OA开放访问", "出版商", "涉及的研究方向", "出版国家或地区", "出版语言", "出版周期", "出版年份", "WOS期刊SCI分区", "平均审稿速度", "平均录用比例"]:
                field_value = tr.css("tr > td:nth-child(2)::text").get()
            elif field_name in ["期刊名字"]:
                field_value = tr.css("tr > td:nth-child(2) > span:nth-child(1) > a::text").get()
            elif field_name in ["期刊官方网站"]:
                field_value = tr.css("tr > td:nth-child(2) > a::text").get()
            elif field_name in ["中科院SCI期刊分区"] and cas_first: # 基础版
                field_value = tr.css("tr > td:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(1) > span:nth-child(2)::text").get()
                cas_first = False
            result[field_name] = field_value
    return result

async def searchInLetpubBatch(query_list: List[str], savepath: str, headless: bool =False, gap: int =30):
    """在Letpub网页中批量搜索关键词列表query_list
    Args:
        query_list(List[str]): 待搜索的关键词列表
        savepath(str): 结果保存路径(csv格式)
        headless(bool): 是否以无头模式运行
        gap(int): 相邻两次查询的时间间隔
    """
    logger.info(f"Total {len(query_list)} item to query.")
    result = []
    with open(savepath, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["期刊名字", "期刊ISSN", "h-index", "期刊官方网站", "是否OA开放访问", "出版商", "涉及的研究方向", "出版国家或地区", "出版语言", "出版周期", "出版年份", "WOS期刊SCI分区", "中科院SCI期刊分区", "平均审稿速度", "平均录用比例", "详情", "备注", "key", "state"])
        j = 1
        for i, query in enumerate(query_list):
            try:
                # 过滤arxiv
                if 'arxiv' in str(query).lower():
                    logger.info(f"skip query for '{query}'")
                    row = {
                        "期刊名字": query,
                        "备注": f"属于arxiv",
                        "key": j,
                        "state": "跳过",
                    }
                    result.append(row)
                    j += 1
                    continue
                # 过滤会议
                if isConference(query):
                    logger.info(f"skip query for '{query}' (conference)")
                    row = {
                        "期刊名字": query,
                        "备注": f"属于会议",
                        "key": j,
                        "state": "跳过",
                    }
                    result.append(row)
                    j += 1
                    continue
                logger.info(f"querying '{query}'")
                out = await searchInLetpub(query, headless=headless)
                if out is not None:
                    row = out[0]
                    row['key'] = j
                    j += 1
                    # temp = searchInCCF(query)
                    # row['CCF评级'] = temp['ccf_level']
                    ic(i, row)
                    result.append(row)
                    writer.writerow(row)
                    f.flush()
                    if i != len(query_list)-1:
                        time.sleep(gap)
            except:
                logger.error("发生错误!")
                logger.error(traceback.format_exc())
    return result

