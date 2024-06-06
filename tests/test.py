class Screen:

    class SearchCommand:

        def execute(self):
            print('test')

    class ExitCommand:

        def execute(self):
            print('exit')



screen = Screen()
screen.SearchCommand().execute()