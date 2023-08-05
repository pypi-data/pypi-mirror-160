import setuptools

setuptools.setup(
    name = "myfiglet",
    author = "Harsh Gupta",
    version='0.0.3',
    author_email = "harshnkgupta@gmail.com",
    description = "FIGlet Using Python",
    long_description="This program can be used to display FIGlet fonts using python.\nThis is a simple,standalone and easy to understand module with zero dependency on external packages.With just 300 lines of code this is a beginner friendly module.\n\nBest use case :: Can be used in unison with different programs to make them more lively and attarctive: \n\nSyntax:\n\n>>>import myfiglet\n\n>>>myfiglet.display(<input_string>,<symbol>)\n\nType >>>myfiglet.help() for further help.",
    packages=['myfiglet'],
    install_requires=[]
    )
