class Colors:
  def __init__(self):
    self.blackk = "\u001b[30m"
    self.redd = "\u001b[31m"
    self.greenn = "\u001b[32m"
    self.yelloww = "\u001b[33m"
    self.bluee = "\u001b[34m"
    self.magentaa = "\u001b[35m"
    self.cyann = "\u001b[36m"
    self.whitee = "\u001b[37m"
    self.resett = "\u001b[0m"

  def black(self, *, text):
    return f"{self.blackk}{text}"

  def red(self, *, text):
    return f"{self.redd}{text}"

  def green(self, *, text):
    return f"{self.greenn}{text}"

  def yellow(self, *, text):
    return f"{self.yelloww}{text}"

  def blue(self, *, text):
    return f"{self.bluee}{text}"

  def magenta(self, *, text):
    return f"{self.magentaa}{text}"

  def cyan(self, *, text):
    return f"{self.cyann}{text}"

  def white(self, *, text):
    return f"{self.whitee}{text}"

  def reset(self, *, text):
    return f"{self.resett}{text}"