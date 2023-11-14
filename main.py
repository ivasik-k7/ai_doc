#!/usr/bin/env python3

import os
import re
import asyncio
import argparse
from openai import (
    OpenAI,
    RateLimitError,
    APIConnectionError,
    APIStatusError,
)
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),
    **os.environ,
}

client = OpenAI(
    api_key=config["OPENAI_API_KEY"],
)


class OpenAICompletions:
    @staticmethod
    def raw_doc(prompt: str):
        try:
            response = client.chat.completions.with_raw_response.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Your main task is to generate asciidoc documentation based on a query. You need to generate an answer that is valid enough to be automatically recorded in the document whose content you are going to generate. This content is documentation about a specific functionality that you need to describe in as much detail as possible. The documentation should be written follow the latest best practices of writing the documentation. Including description, use cases, etc. Content:\n {prompt}",
                    },
                ],
                model=config["OPENAI_MODEL"],
            )
            completion = response.parse()
            return completion.choices[0].message.content
        except APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)

    @staticmethod
    def raw_puml(prompt: str):
        try:
            response = client.chat.completions.with_raw_response.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Your main task is to describe the plantuml diagram in as accessible and detailed a way as possible, focusing on the content. Be sure to use simple, free keywords to describe the details that are officially provided by plantuml.  The name of the documentation should be based on its content, e.g. @startuml content_example. The values you output should be valid so that they can be written to a file immediately. Content:\n {prompt}",
                    },
                ],
                model=config["OPENAI_MODEL"],
            )

            completion = response.parse()
            return completion.choices[0].message.content
        except APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)


def read_file_content(file_path) -> str:
    try:
        with open(file_path, "r") as file:
            content = file.read()

        return content

    except FileNotFoundError:
        print(f"File not found at path: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


async def read_passed_files(file_paths):
    content = ""
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            content += f"Path:\n{file_path} Content:\n{file.read()} \n"

    return content


def extract_sections(content):
    pattern = r"^(##|==)\s*(\w+\s*\w*)\n(.*?)(?=\n(##|==)|\Z)"
    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)

    sections = {match.group(2): match.group(3).strip() for match in matches}

    return sections


def write_documentation_file(
    folder_path: str,
    content: str,
    file_name: str,
):
    try:
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, file_name)

        # Write content to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"File '{file_name}' successfully created in '{folder_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_puml_files(content: str):
    result = extract_sections(content)

    if result:
        for example in result:
            description = result[example]
            file_name = example.lower().replace(" ", "_").replace("\n", "").strip()
            response = OpenAICompletions.raw_puml(description)

            write_documentation_file(
                folder_path="./artifacts",
                content=response,
                file_name=f"{file_name}.pu",
            )


async def main():
    parser = argparse.ArgumentParser(
        description="Read content from multiple files.",
    )

    parser.add_argument(
        "-f",
        "--filename",
        help="The output name of the file",
        default="documentation",
    )

    parser.add_argument(
        "file_paths",
        nargs="+",
        help="Paths to the files to be processed",
    )

    args = parser.parse_args()

    values = args.file_paths

    file_name = args.filename
    content = await read_passed_files(values)

    if content:
        response = OpenAICompletions.raw_doc(prompt=content)
        if response:
            write_documentation_file(
                content=response,
                file_name=f"{file_name}.adoc",
                folder_path="./artifacts",
            )

            write_puml_files(response)


if __name__ == "__main__":
    asyncio.run(main())
