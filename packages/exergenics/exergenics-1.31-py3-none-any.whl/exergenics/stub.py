from exergenics import ExergenicsApi

api = ExergenicsApi("john.christian@hashtagtechnology.com.au", "M1nd0v3rM4tt3r", False)

if not api.authenticate():
    exit("couldnt authenticate")

api.putFile("JC-TEST-PLANT-1", "http://file.com/", "bowl-chart", "Bowl Chart")
