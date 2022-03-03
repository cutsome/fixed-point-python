.PHONY: test
test:
	@python -m unittest tests.test_fix32

.PHONY: seed
data:
	@python seed.py

.PHONY: debug
debug:
	@python fix32.py
