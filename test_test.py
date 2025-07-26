import pytest
import shlex

from main import main

result_case_1 = ('handler                     total    avg_response_time\n'
'------------------------  -------  -------------------\n'
'/api/homeworks/...             71                0.158\n'
'/api/context/...               21                0.043\n'
'/api/specializations/...        6                0.035\n'
'/api/users/...                  1                0.072\n'
'/api/challenges/...             1                0.056')

result_case_2 = ('handler                     total    avg_response_time\n'
 '------------------------  -------  -------------------\n'
 '/api/homeworks/...          55312                0.093\n'
 '/api/context/...            43928                0.019\n'
 '/api/specializations/...     8335                0.052\n'
 '/api/challenges/...          1476                0.078\n'
 '/api/users/...               1447                0.066')

result_case_3 = ('handler                     total    avg_response_time\n'
 '------------------------  -------  -------------------\n'
 '/api/homeworks/...           3521                0.095\n'
 '/api/context/...             2564                0.023\n'
 '/api/specializations/...      570                0.056\n'
 '/api/users/...                101                0.07\n'
 '/api/challenges/...           101                0.087')

test_cases: list[tuple] = [
    ('--file example_log/example1.log --report average', result_case_1),
    ('--file example_log/example1.log example_log/example2.log --report average', result_case_2),
    ('--file example_log/example1.log example_log/example2.log --report average --date 2025-22-06', result_case_3)
]


@pytest.mark.parametrize('command, expected_output', test_cases)
def test_main(capsys, command, expected_output):
    main(shlex.split(command))
    output = capsys.readouterr().out.rstrip()
    assert output == expected_output

def test_main_for_missing_parameters(capsys):
    with pytest.raises(SystemExit):
        main(shlex.split('--file example_log/example1.log example_log/example2.log'))
    out, err = capsys.readouterr()