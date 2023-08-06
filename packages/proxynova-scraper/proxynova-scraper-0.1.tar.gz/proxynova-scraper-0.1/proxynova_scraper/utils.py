from re import sub

def _to_camelcase(s):
  """
    Transforms a string to camelcase
    Arguments:
      s: string
    Returns:
      A string in camelcase format
  """
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])

def _replace_chars(content: str):
  """
    Removes all the characters from a string
    Arguments:
      content: a string
    Returns:
      The string without special characters
  """
  return sub(r'[^\w]','',content)
