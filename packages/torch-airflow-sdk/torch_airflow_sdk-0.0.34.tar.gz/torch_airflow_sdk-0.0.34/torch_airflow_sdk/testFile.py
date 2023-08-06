

# def testfunc(*args, **kwargs):
#     global success_callback_func
#     success_callback_func = kwargs.pop('on_success_callback', None)
#     is_override_success_callback = kwargs.pop('override_success_callback', False)
#
#     if success_callback_func is not None and not is_override_success_callback:
#         success_callback_func = "merged_callback"
#     elif not is_override_success_callback:
#         success_callback_func = "old_default_callback"
#
#     print(success_callback_func)

def testfunc(*args, **kwargs):
    global success_callback_func
    success_callback_func = kwargs.pop('on_success_callback', 'old_default_callback')
    is_override_success_callback = kwargs.pop('override_success_callback', False)

    if not is_override_success_callback:
        success_callback_func = "merged_callback"
    elif not is_override_success_callback:
        success_callback_func = "old_default_callback"

    print(success_callback_func)

if __name__ == "__main__":
    print("passing empty args")
    testfunc()
    print("passing is_override_success_callback args")
    testfunc(override_success_callback=True)
    print("passing on_success_callback args")
    testfunc(on_success_callback="test_merged")
    print("passing both args")
    testfunc(on_success_callback="test_passed_function", override_success_callback=True)
