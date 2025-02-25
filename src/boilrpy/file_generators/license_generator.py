from datetime import datetime
from boilrpy.file_generators.base_generator import BaseGenerator


class LicenseGenerator(BaseGenerator):
    """
    Generator for license files.
    """

    def generate(self, *args, **kwargs) -> str:
        """
        Generate the content for the license file.

        :param license_name: Name of the license
        :param author: Name of the author
        :return: Content of the license file
        """
        license_name = args[0] if args else ""
        author = args[1] if args else ""
        license_strategy = self._get_license_strategy(license_name)
        return license_strategy.generate(author)

    def _get_license_strategy(self, license_name: str):
        """
        Get the appropriate license strategy based on the license name.

        :param license_name: Name of the license
        :return: LicenseStrategy object
        """
        strategies = {
            "mit": MITLicenseStrategy(),
            "apache": ApacheLicenseStrategy(),
            "gpl": GPLLicenseStrategy(),
            "bsd": BSDLicenseStrategy(),
        }
        return strategies.get(license_name.lower(), MITLicenseStrategy())


class LicenseStrategy:
    """
    Base class for license strategies.
    """

    def generate(self, *args) -> str:
        """
        Generate the license text.

        :param author: Name of the author
        :param kwargs: Additional keyword arguments
        :return: License text
        """
        author = args[0] if args else ""
        year = str(datetime.now().year)
        return self._get_template().format(year=year, author=author)

    def _get_template(self) -> str:
        """
        Get the license template.
        """
        raise NotImplementedError


class MITLicenseStrategy(LicenseStrategy):
    """
    Strategy for generating MIT license.
    """

    def _get_template(self) -> str:
        return """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class ApacheLicenseStrategy(LicenseStrategy):
    """
    Strategy for generating Apache license.
    """

    def _get_template(self) -> str:
        return """Apache License

Copyright {year} {author}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class GPLLicenseStrategy(LicenseStrategy):
    """
    Strategy for generating GPL license.
    """

    def _get_template(self) -> str:
        return """GPL License

Copyright {year} {author}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""


class BSDLicenseStrategy(LicenseStrategy):
    """
    Strategy for generating BSD license.
    """

    def _get_template(self) -> str:
        return """BSD License

Copyright (c) {year} {author}
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
"""
