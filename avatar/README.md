# avatar

This is a micro api for providing initials avatars -- like the one used in Gmail.
This is a DETA service but could be easily adjusted to work in other environments.

You can run it without servers by sining up on [DETA](https://deta.sh) for free.

## Use

This service takes input as query parameters:

- `i` for the initials, use 1-3 chars for optimal results.
- `c` for the primary color. Will chose a random color if omitted.
- `cc` for an additional color, will result in a gradient.

## Preview

![alt text](avatar_onecolor.png "One color avatar")
![alt text](avatar_gradient.png "Gradient (two colors avatar)")
