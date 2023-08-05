class Colors:
  def __init__(self):
    self.black = "\u001b[30m"
    self.red = "\u001b[31m"
    self.green = "\u001b[32m"
    self.yellow = "\u001b[33m"
    self.blue = "\u001b[34m"
    self.magenta = "\u001b[35m"
    self.cyan = "\u001b[36m"
    self.white = "\u001b[37m"
    self.reset = "\u001b[0m"

  def black(self, *, text):
    return f"{self.black}{text}"

  def red(self, *, text):
    return f"{self.red}{text}"

  def green(self, *, text):
    return f"{self.green}{text}"

  def yellow(self, *, text):
    return f"{self.yellow}{text}"

  def blue(self, *, text):
    return f"{self.blue}{text}"

  def magenta(self, *, text):
    return f"{self.magenta}{text}"

  def cyan(self, *, text):
    return f"{self.cyan}{text}"

  def white(self, *, text):
    return f"{self.white}{text}"

  def reset(self, *, text):
    return f"{self.reset}{text}"