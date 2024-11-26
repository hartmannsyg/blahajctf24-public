Recognise that the password is being checked backwards due to `std` instruction call. Patch out the wait by zeroing out `0x0f73` and `0x1400` from the binary so that the sleep becomes 0 seconds rather than 3 days.

Flag: `blahaj{B105_INTs}`