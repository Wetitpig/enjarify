#include <stdlib.h>
#include <stdint.h>

uint16_t ru16(char *sto)
{
	union {
		uint16_t res;
		char inter[2];
	} u;
	memcpy(u.inter, sto, 2);
#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
	return u.res;
#else
	return __builtin_bswap16(u.res);
#endif
}

uint32_t ru32(char *sto)
{
	union {
		uint32_t res;
		char inter[4];
	} u;
	memcpy(u.inter, sto, 4);
#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
	return u.res;
#elif __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
	return __builtin_bswap32(u.res);
#else
	return ((u.res & 0x00FF00FF) << 8) | ((u.res & 0xFF00FF00) >> 8);
#endif
}

uint64_t ru64(char *sto)
{
	union {
		uint64_t res;
		char inter[8];
	} u;
	memcpy(u.inter, sto, 8);
#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
	return u.res;
#else
	return __builtin_bswap64(u.res);
#endif
}
