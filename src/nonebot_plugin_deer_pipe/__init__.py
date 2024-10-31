from .database import attend, reattend
from .image import generate_image
import base64
from datetime import datetime
from hoshino import Service
from hoshino.typing import CQEvent


sv_help = '''
发送🦌以进行签到
'''.strip()

sv = Service(
    name="🦌管签到",  # 功能名
    visible=True,  # 可见性
    enable_on_default=True,  # 默认启用
    bundle="娱乐",  # 分组归类
    help_=sv_help,  # 帮助说明
)


@sv.on_fullmatch("🦌")
async def luguan(bot, event: CQEvent):
    sid = event.self_id
    gid = str(event.group_id)
    card: dict = await bot.get_group_member_info(group_id=gid, user_id=sid)
    name: str = (card.get("card") or card.get("nickname") or str(sid))
    now: datetime = datetime.now()
    deer: dict[int, int] = await attend(now, str(sid))
    img: bytes = generate_image(now, name, deer)
    await bot.send(
        event,
        f'成功🦌了[CQ:image,file=base64://{base64.b64encode(img).decode()}]',
        at_sender=True
    )


@sv.on_prefix("补🦌")
async def bulu(bot, event: CQEvent):
    sid = event.self_id
    gid = str(event.group_id)
    card: dict = await bot.get_group_member_info(group_id=gid, user_id=sid)
    name: str = (card.get("card") or card.get("nickname") or str(sid))
    now: datetime = datetime.now()
    try:
        day: int = int(event.message.extract_plain_text().strip().split(" ")[-1])
    except Exception:
        day: int = -1
    if day <= 0 or day >= now.day:
        await bot.send(event, "不是合法的补🦌日期捏", at_sender=True)
        return

    ok, deer = await reattend(now, day, str(sid))
    img: bytes = generate_image(now, name, deer)
    await bot.send(
        event,
        f'{"成功补🦌" if ok else "只能补🦌没有🦌的日子捏"}[CQ:image,file=base64://{base64.b64encode(img).decode()}]',
        at_sender=True
    )
