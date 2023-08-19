import pygame
from aiohttp import web

class ExternalInputController(object):
    CUSTOM_EVENT_ID = pygame.USEREVENT + 1

    # Nothing to do
    def __init__(self):
        print("ExternalInputController::init")

    @staticmethod
    async def handle(request):
        print("ExternalInputController::handle - Received a request!")
        command = request.rel_url.query['command']

        text = "Received command, " + command

        print("ExternalInputController::handle - Request served")
        # Command should be a number between 0 and 63 describing the location of the click inside the matrix
        if command and str.isnumeric(command):
            custom_event = pygame.event.Event(ExternalInputController.CUSTOM_EVENT_ID, command=command)
            # Post the custom event to the event queue
            pygame.event.post(custom_event)
        else:
            print("ExternalInputController::handle - Received non-numeric command")
        return web.Response(text=text)

    async def start_server(self):
        print("ExternalInputController::start_server")
        app = web.Application()
        app.router.add_get('/', ExternalInputController.handle)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()
