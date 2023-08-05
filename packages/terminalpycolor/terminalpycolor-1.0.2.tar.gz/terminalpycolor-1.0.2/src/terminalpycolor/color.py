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

  def black(self, *text):
    nn = text
    hh = ",".join([str(nn) for nn in list(nn)])
    return f"{self.blackk}{hh}"

  def red(self, *text):
    nn = text
    hh = ",".join([str(nn) for nn in list(nn)])
    return f"{self.redd}{hh}"

  def green(self, *text):
    nn = text
    hh = ",".join([str(nn) for nn in list(nn)])
    return f"{self.greenn}{hh}"

  def yellow(self, *text):
    nn = text
    hh = ",".join([str(nn) for nn in list(nn)])
    return f"{self.yelloww}{hh}"

  def blue(self, *text):
    nn = text
    hh = ",".join([str(nn) for nn in list(nn)])
    return f"{self.bluee}{hh}"

  def magenta(self, *text):
    nn = text
    hh = ",".join([str(nn) for nn in list(nn)])
    return f"{self.magentaa}{hh}"

  def cyan(self, *text):
    nn = text
    hh = ",".join([str(nn) for nn in list(nn)])
    return f"{self.cyann}{hh}"

  def white(self, *text):
    nn = text
    hh = ",".join([str(nn) for nn in list(nn)])
    return f"{self.whitee}{hh}"

  def reset(self, *text):
    nn = text
    hh = ",".join([str(nn) for nn in list(nn)])
    return f"{self.resett}{hh}"