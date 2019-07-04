#include <stdint.h>

int64_t signExtend(uint64_t val, size_t size)
{
	int64_t result = val;
	if(val >> (size - 1))
		result -= (1 << size);
	return result;
}
