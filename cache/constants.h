// TODO make this a real value lol
#include <cstdio>
#define STACK_FLOOR 0x999999999999999

#define DEBUG 0

#define PAGE_SIZE 4096

#define PAGE_ALIGN_ADDR(addr) (addr & ~(PAGE_SIZE - 1))

#define RETURN_IF_ERROR(expr)                                                  \
  if (expr != Status::OK) {                                                    \
    return expr;                                                               \
  }

#define DEBUG_CHECK(expr)                                                      \
  if (DEBUG && !(expr)) {                                                      \
    return Status::BAD;                                                        \
  }

#define DEBUG_LOG(s)                                                           \
  if (DEBUG) {                                                                 \
    std::cout << s;                                                            \
  }

#define PBSTR "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
#define PBWIDTH 60

inline void printProgress(double percentage) {
    int val = (int) (percentage * 100);
    int lpad = (int) (percentage * PBWIDTH);
    int rpad = PBWIDTH - lpad;
    printf("\r%3d%% [%.*s%*s]", val, lpad, PBSTR, rpad, "");
    fflush(stdout);
}
