def clean(s):
    return (s.replace("#", "\#")
             .replace("{", "\{")
             .replace("}", "\}")
             .replace(".", "\.")
             .replace("(", "\(")
             .replace(")", "\)")
             .replace("_", "\_")
             .replace("-", "\-")
             .replace("<", "\<")
             .replace(">", "\>"))
