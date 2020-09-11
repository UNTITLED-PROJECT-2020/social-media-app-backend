# imports
from channels.routing import ProtocolTypeRouter

# routing or application to use channels server for messaging
application = ProtocolTypeRouter({
    # (http -> django views is added by default)

    # # WebSocket chat handler

    # "websocket": AuthMiddlewareStack(
    #     URLRouter([
    #         url(r"^chat/admin/$", AdminChatConsumer),
    #         url(r"^chat/$", PublicChatConsumer),
    #     ])
    # ),

    # # Using the third-party project frequensgi, which provides an APRS protocol
    # "aprs": APRSNewsConsumer,
})
