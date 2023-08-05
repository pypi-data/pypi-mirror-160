import re
from laboro.logic.parser import Parser


class Processor:
  @staticmethod
  def process(context, statement):
    word_ptn = re.compile(r"\$store\$\w+")
    store_ptn = re.compile(r"^\$store\$")
    vars = re.findall(word_ptn, statement)
    values = [str(context.get(re.sub(store_ptn, "", var))) for var in vars]
    for var, value in zip(vars, values):
      var_ptn = re.compile(var.replace("$", r"\$"))
      statement = re.sub(var_ptn, value, statement)
    if context.get_step_item() is not None:
      pattern = re.compile(r"\$step_item\$")
      statement = re.sub(pattern, str(context.get_step_item()), statement)
    if context.get_action_item() is not None:
      pattern = re.compile(r"\$action_item\$")
      statement = re.sub(pattern, str(context.get_action_item()), statement)
    if context.get_method_item() is not None:
      pattern = re.compile(r"\$method_item\$")
      statement = re.sub(pattern, str(context.get_method_item()), statement)
    file_ptn = re.compile(r"\$file\$")
    filepath = f"{context.workspace.workspace_path}/"
    statement = re.sub(file_ptn, filepath, statement)
    datafile_ptn = re.compile(r"\$datafile\$")
    datafile_path = f"{context.workspace.workspace_dir}/"
    statement = re.sub(datafile_ptn, datafile_path, statement)
    return Parser().eval(statement)

  @staticmethod
  def process_arg(context, value):
    store_ptn = re.compile(r"\$store\$\w+")
    for key in re.findall(store_ptn, value):
      val = context.get(key.replace("$store$", ""))
      value = value.replace(key, str(val))
    if context.get_step_item() is not None:
      pattern = re.compile(r"\$step_item\$")
      value = re.sub(pattern, str(context.get_step_item()), value)
    if context.get_action_item() is not None:
      pattern = re.compile(r"\$action_item\$")
      value = re.sub(pattern, str(context.get_action_item()), value)
    if context.get_method_item() is not None:
      pattern = re.compile(r"\$method_item\$")
      value = re.sub(pattern, str(context.get_method_item()), value)
    file_ptn = re.compile(r"\$file\$")
    filepath = f"{context.workspace.workspace_path}/"
    value = re.sub(file_ptn, filepath, value)
    datafile_ptn = re.compile(r"\$datafile\$")
    datafile_path = f"{context.workspace.workspace_dir}/"
    value = re.sub(datafile_ptn, datafile_path, value)
    return Parser().literal_eval(value)
