import argparse
from hashlib import sha1


def compute_hash(email):
    return sha1(email.encode("utf-8")).hexdigest()


def compute_certificate_id(email):
    email_clean = email.lower().strip()
    return compute_hash(email_clean + "_")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute certificate ID.")
    parser.add_argument(
        "email", type=str, help="Email address to compute the certificate ID for."
    )
    args = parser.parse_args()

    cohort = 2024
    course = "dezoomcamp"
    your_id = compute_certificate_id(args.email)
    url = f"https://certificate.datatalks.club/{course}/{cohort}/{your_id}.pdf"
    print(url)
