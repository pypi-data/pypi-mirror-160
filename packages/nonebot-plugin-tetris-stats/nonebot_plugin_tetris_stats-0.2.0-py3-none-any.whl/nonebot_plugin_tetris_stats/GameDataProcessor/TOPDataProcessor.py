from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GROUP, MessageEvent
from nonebot.matcher import Matcher
from nonebot.log import logger

from typing import Any, Mapping
from asyncio import gather
from re import I

from ..Utils.Request import request

from ..Utils.MessageAnalyzer import handleBindMessage, handleStatsQueryMessage
from ..Utils.SQL import queryBindInfo, writeBindInfo

topBind = on_regex(pattern=r'^top绑定|^topbind', flags=I, permission=GROUP)
topStats = on_regex(pattern=r'^top查|^topstats', flags=I, permission=GROUP)


@topBind.handle()
async def bindTOPUser(event: MessageEvent, matcher: Matcher):
    await matcher.finish(message='TODO')


@topStats.handle()
async def handleTOPStatsQuery(event: MessageEvent, matcher: Matcher):
    await matcher.finish(message='TODO')
