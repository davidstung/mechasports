These are examples from SdFat V1 for compatibility tests.

All except SdFatRawWrite compiled without change.

SdFatRawWrite needed a (uint8_t*) cast on this line:

  uint8_t* pCache = (uint8_t*)volume.cacheClear();

I have not run detailed tests yet.
