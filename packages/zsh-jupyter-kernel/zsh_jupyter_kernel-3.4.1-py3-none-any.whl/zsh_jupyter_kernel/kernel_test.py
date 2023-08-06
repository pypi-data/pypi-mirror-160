import unittest
import jupyter_kernel_test

class ZshKernelTests (jupyter_kernel_test.KernelTests):
    kernel_name = "zsh"
    language_name = "zsh"
    file_extension = ".zsh"

    code_hello_world = "<<<'hello, world'"

    code_stderr = ">&2 print error"

    # completion_samples = [
    #     {
    #         'text': 'print',
    #         'matches': [
    #             'printf',
    #             'printenv',
    #             # not sure why the following ones are included
    #             'printf',
    #             'print',
    #         ],
    #     },
    # ]
    complete_code_samples = [
        'print 1',
        "f(){<<<2}\nf\n\n\n",
    ]
    incomplete_code_samples = [
        "print '3",
    ]
    invalid_code_samples = [
    ]

    code_execute_result = [
        {
            'code': "<<< $((1+2+3))",
            'result': "6",
        }
    ]

if __name__ == '__main__':
    unittest.main()

# Reference
# https://github.com/jupyter/jupyter_kernel_test
