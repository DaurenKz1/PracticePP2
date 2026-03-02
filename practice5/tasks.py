import re


# 1
pattern1 = "ab*"
print(bool(re.fullmatch(pattern1, "a")))
print(bool(re.fullmatch(pattern1, "abbb")))


# 2
pattern2 = "ab{2,3}"
print(bool(re.fullmatch(pattern2, "abb")))
print(bool(re.fullmatch(pattern2, "abbb")))


# 3
pattern3 = "[a-z]+_[a-z]+"
text3 = "hello_world test_value OK_Test"
print(re.findall(pattern3, text3))


# 4
pattern4 = "[A-Z][a-z]+"
text4 = "Hello World TEST Apple"
print(re.findall(pattern4, text4))


# 5
pattern5 = "a.*b"
print(bool(re.fullmatch(pattern5, "ab")))
print(bool(re.fullmatch(pattern5, "axxxb")))


# 6
text6 = "Hello, world. Test string"
print(re.sub("[ ,\.]", ":", text6))


# 7
def snake_to_camel(text):
    return re.sub("_([a-z])", lambda m: m.group(1).upper(), text)

print(snake_to_camel("hello_world_test"))


# 8
text8 = "HelloWorldTest"
print(re.split("(?=[A-Z])", text8))


# 9
text9 = "HelloWorldTest"
print(re.sub("([A-Z])", " \1", text9).strip())


# 10
def camel_to_snake(text):
    return re.sub("([A-Z])", "_\1", text).lower().strip("_")

print(camel_to_snake("helloWorldTest"))