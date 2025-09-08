
/*
 * Example for a unit test using the ztest framework.
 */

#include <ztest.h>

static void test_assert(void) {
    zassert_true(1, "1 was false");
}

void test_main(void) {
    ztest_test_suite(framework_tests,
        ztest_unit_test(test_assert)
    );
    ztest_run_test_suite(framework_tests);
}
