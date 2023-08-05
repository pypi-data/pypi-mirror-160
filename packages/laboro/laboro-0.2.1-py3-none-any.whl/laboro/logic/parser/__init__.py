import logging
from ast import literal_eval
from asteval import Interpreter
from laboro.logger import LaboroLogger

logging.setLoggerClass(LaboroLogger)
logger = logging.getLogger("laboro.main")


class Parser:
  @staticmethod
  def eval(expression):
    try:
      return Interpreter().eval(expression,
                                show_errors=False,
                                raise_errors=True)
    except SyntaxError as err:
      logger.critical(f"Invalid syntax for expression: {expression}")
      raise err

  @staticmethod
  def literal_eval(expression):
    try:
      return literal_eval(expression)
    except (ValueError, SyntaxError):
      return expression
