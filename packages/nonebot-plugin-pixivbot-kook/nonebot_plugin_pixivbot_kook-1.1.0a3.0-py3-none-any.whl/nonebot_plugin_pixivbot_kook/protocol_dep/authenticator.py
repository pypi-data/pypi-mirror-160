from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.protocol_dep.authenticator import AuthenticatorManager, \
    Authenticator as BaseUserAuthenticator

from .post_dest import PostDestination


@context.require(AuthenticatorManager).register
class Authenticator(BaseUserAuthenticator):
    @classmethod
    def adapter(cls) -> str:
        return "kaiheila"

    async def group_admin(self, post_dest: PostDestination) -> bool:
        # 搞不懂怎么实现
        return True
