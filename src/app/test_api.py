import argparse
import requests


# Parser
parser = argparse.ArgumentParser(description='Process some tests.')
parser.add_argument('--api_key', type=str, required=False, default='', help='API key for accessing the service')

args = parser.parse_args()


# Headers
headers = {
    'x-api-key': args.api_key
}


def test_api():
    # Test-secure-endpoint
    response = requests.get("http://localhost:5000/test-secure-endpoint", headers=headers)
    print(response.text)

    # Test-secure-endpoint limit
    response = requests.get("http://localhost:5000/test-secure-endpoint", headers=headers)
    response = requests.get("http://localhost:5000/test-secure-endpoint", headers=headers)
    print(response.text)



if __name__ == "__main__":
    test_api()