import pytest
from boilrpy.utils.string_formatter import StringFormatter


class TestStringFormatter:

    @pytest.mark.parametrize(
        "input_string, expected",
        [
            # Already camelCase (first return)
            ("alreadyCamelCase", "alreadyCamelCase"),
            ("AnotherCamelCase", "anotherCamelCase"),
            ("a", "a"),
            ("ab", "ab"),
            ("a1", "a1"),
            # CamelCase (only first letter lowered)
            ("CamelCase", "camelCase"),
            ("AnotherCamelCase", "anotherCamelCase"),
            # Main conversion logic
            ("test_string", "testString"),
            ("TEST_STRING", "testString"),
            ("Test String", "testString"),
            ("testString", "testString"),
            ("test-string", "testString"),
            ("test_string_with_numbers123", "testStringWithNumbers123"),
            # Edge cases
            ("A", "a"),
            ("123", "123"),
            ("123_test", "123Test"),
            ("TEST", "tEST"),
            ("T_E_S_T", "tEST"),
            ("__test__string__", "testString"),
        ],
    )
    def test_to_camel_case(self, input_string, expected):
        assert StringFormatter.to_camel_case(input_string) == expected

    @pytest.mark.parametrize(
        "input_string, expected",
        [
            # Already snake_case (first return)
            ("already_snake_case", "already_snake_case"),
            ("another_snake_case", "another_snake_case"),
            ("a", "a"),
            ("a_b_c", "a_b_c"),
            # Main conversion logic
            ("TestString", "test_string"),
            ("testString", "test_string"),
            ("test_string", "test_string"),
            ("TEST_STRING", "test_string"),
            ("Test String", "test_string"),
            ("testStringWithNumbers123", "test_string_with_numbers123"),
            # Edge cases
            ("A", "a"),
            ("123", "123"),
            ("123Test", "123_test"),
            ("TEST", "test"),
            ("T_E_S_T", "t_e_s_t"),
            ("__Test__String__", "_test_string_"),
            # Test cases for the final substitution
            ("Test-String", "test_string"),
            ("Test.String", "test_string"),
            ("Test@String", "test_string"),
            ("Test#String", "test_string"),
            ("Test$String", "test_string"),
            ("Test%String", "test_string"),
            ("Test^String", "test_string"),
            ("Test&String", "test_string"),
            ("Test*String", "test_string"),
            ("Test(String)", "test_string_"),
            ("Test+String", "test_string"),
            ("Test=String", "test_string"),
            ("Test|String", "test_string"),
            ("Test:String", "test_string"),
            ("Test;String", "test_string"),
            ("Test'String'", "test_string_"),
            ('Test"String"', "test_string_"),
            ("Test<String>", "test_string_"),
            ("Test,String", "test_string"),
            ("Test?String!", "test_string_"),
            ("Test~~~String", "test_string"),
            ("___Test___String___", "_test_string_"),
            ("   Test   String   ", "test_string"),
        ],
    )
    def test_to_snake_case(self, input_string, expected):
        assert StringFormatter.to_snake_case(input_string) == expected

    @pytest.mark.parametrize(
        "project_name, use_camel_case, expected",
        [
            # CamelCase
            ("test_project", True, "testProject"),
            ("TestProject", True, "testProject"),
            ("test-project", True, "testProject"),
            ("TEST_PROJECT", True, "testProject"),
            ("CamelCase", True, "camelCase"),
            # snake_case
            ("test_project", False, "test_project"),
            ("TestProject", False, "test_project"),
            ("test-project", False, "test-project"),
            ("TEST_PROJECT", False, "test_project"),
            ("CamelCase", False, "camel_case"),
            # Edge cases
            ("A", True, "a"),
            ("A", False, "a"),
            ("123_test", True, "123Test"),
            ("123_test", False, "123_test"),
        ],
    )
    def test_format_project_name(self, project_name, use_camel_case, expected):
        assert (
            StringFormatter.format_project_name(project_name, use_camel_case)
            == expected
        )

    def test_to_camel_case_first_return(self):
        input_string = "alreadyCamelCase"
        result = StringFormatter.to_camel_case(input_string)
        assert result == input_string
        assert result is input_string

    def test_to_snake_case_first_return(self):
        input_string = "already_snake_case"
        result = StringFormatter.to_snake_case(input_string)
        assert result == input_string
        assert result is input_string
