import sys

def show_exception_and_exit(exc_type, exc_value, tb):
    """
    This code defines a function `show_exception_and_exit` which is used to handle uncaught exceptions in
     a Python program. When an uncaught exception occurs, this function is called with the exception type,
      exception value, and traceback as arguments.

    The function performs the following steps:

    1. It imports the necessary modules: `basicConfig` and `error` from the `logging` module, and `Path` from the `pathlib` module.

    2. It creates a `Path` object called `log_file_name` with the path './unhandled_exception.log'.

    3. If the `log_file_name` already exists, it is deleted using the `unlink()` method. Otherwise, no action is taken.

    4. It tries to configure the logging module to write the error messages to the `log_file_name`. The logging level is set to 'ERROR'.

    5. If an exception occurs while configuring the logging, a message 'could not log unhandled exception due to error' is printed.

    6. If the logging was successfully configured, an error message 'Uncaught exception' is logged using the `error()` method of the logging module. The exception information is passed using the `exc_info` parameter.

    7. The `sys.__excepthook__` function is called with the exception type, exception value, and traceback. This will print the exception information to the console.

    8. A message is printed to inform that if the exception could be logged, it is logged in './unhandled_exception.log' even if it does not appear in other log files.

    9. The program waits for the user to press enter to exit.

    10. Finally, the program exits with a status code of -1 using the `sys.exit()` function.
    """
    from logging import basicConfig, error
    from pathlib import Path

    log_file_name = Path('./unhandled_exception.log')
    if log_file_name.is_file():
        log_file_name.unlink()
    else:
        pass
    try:
        basicConfig(filename=log_file_name, level='ERROR')
        error("Uncaught exception", exc_info=(exc_type, exc_value, tb))
    except Exception as e:
        print('could not log unhandled exception due to error.')
    # traceback.print_exception(exc_type, exc_value, tb)
    sys.__excepthook__(exc_type, exc_value, tb)
    print('\n********\n if exception could be logged, it is logged in \'./unhandled_exception.log\''
          ' even if it does not appear in other log files \n********\n')

    #print(getLogger().hasHandlers())
    input("Press enter to exit.")

    # sys.__excepthook__(exc_type, exc_value, tb)
    sys.exit(-1)


sys.excepthook = show_exception_and_exit