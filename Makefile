TEST_PATH=./tests

init:
    pip install -r requirements.txt

test:
    py.test --verbose --color=yes $(TEST_PATH)
