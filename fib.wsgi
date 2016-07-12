import unittest
from urlparse import parse_qs

def application(environ, start_response):
    params = parse_qs(environ.get('QUERY_STRING', ''))
    path = environ.get('PATH_INFO', '').lstrip('/')
    status = '404 NOT FOUND'
    output = 'Endpoint not found on this server: ' + path + '\n'
    if path == 'fibonacci':
        status = '400 BAD REQUEST'
        if 'number' not in params:
            output = 'Missing query parameter: number\n'
        else:
            number = -1
            try:
                number = int(params["number"][0])
            except:
                print("error parsing number")
            if number <= 0:
                output = '"number" must be a positive integer\n'
            else:
                result = fibrange(number)
                if len(result) == 0:
                    status = '500 INTERNAL SERVER ERROR'
                    output = 'The server experienced an error processing fibonacci for: ' + str(number) + '\n'
                else:
                    status = '200 OK'
                    output = str(result) + "\n"
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]

def fibrange(number):
    result = []
    if number <= 0:
        print("cannot process range less than 1: " + str(number))
        return result
    for i in range(number):
        try:
            result.append(fibonacci(i))
        except:
            print("error processing fibonacci: " + str(i))
            result = []
            break
    return result

def fibonacci(numfib):
    if numfib < 0:
        return (pow(-1,(abs(numfib) + 1))) * fibonacci(abs(numfib))
    elif numfib == 0:
        return 0
    elif numfib == 1:
        return 1
    else:
        return fibonacci(numfib - 1) + fibonacci(numfib - 2)

class TestFibonacciNumbers(unittest.TestCase):
    def test_zero(self):
        result = fibonacci(0)
        self.assertEqual(0, result, 'expected 0, received: ' + str(result))
    def test_one(self):
        result = fibonacci(1)
        self.assertEqual(1, result, 'expected 1, received: ' + str(result))
    def test_five(self):
        result = fibonacci(5)
        self.assertEqual(5, result, 'expected 5, received: ' + str(result))
    def test_twenty(self):
        result = fibonacci(20)
        self.assertEqual(6765, result, 'expected 6765, received: ' + str(result))
    def test_neg_five(self):
        result = fibonacci(-5)
        self.assertEqual(5, result, 'expected 5, received: ' + str(result))
    def test_neg_eight(self):
        result = fibonacci(-8)
        self.assertEqual(-21, result, 'expected -21, received: ' + str(result))

class TestFibonacciRange(unittest.TestCase):
    def test_neg(self):
        result = fibrange(-1)
        self.assertEqual(0, len(result), 'expected 0, received: ' + str(len(result)))
    def test_zero(self):
        result = fibrange(0)
        self.assertEqual(0, len(result), 'expected 0, received: ' + str(len(result)))
    def test_one(self):
        result = fibrange(1)
        self.assertEqual(1, len(result), 'expected 1, received: ' + str(len(result)))
        self.assertEqual([0], result, 'expected [0], received: ' + str(result))
    def test_five(self):
        result = fibrange(5)
        self.assertEqual(5, len(result), 'expected 5, received: ' + str(len(result)))
        self.assertEqual([0, 1, 1, 2, 3], result, 'expected [0, 1, 1, 2, 3], received: ' + str(result))

if __name__ == '__main__':
    unittest.main()
