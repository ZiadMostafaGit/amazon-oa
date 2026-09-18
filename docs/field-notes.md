# Field notes

Notes written while preparing, kept verbatim.

---

## Notes & Tips (text from the document)
*Notes · Your own notes from the doc · Field notes*

### On the debugging round (6 failing test cases)

There were six failing test cases that you needed to fix. I used Python, and the language option should be Django. My suggestion is to use AI as much as possible. Paste each failing test case into AI and ask for help. The prompt should tell it not to directly tell you how to fix the code, but you can ask it to point out roughly which function, or which range of lines, the issue might be in. The actual bugs are usually pretty obvious once you look carefully. With the hints from AI, it is not too hard to figure out. The problem I got was about scheduling payments. The mistakes were mostly things like changing `==` to `!=`, changing `(< 0)` to `(<= 0)`, or forgetting to update a variable.

### API review task — follows & notifications

Send you a set of API requirements. Please review whether they are feasible and whether anything needs to be completed or clarified.

The main feature is user-based following and notifications. When a movie is created or published, the system should generate unread notifications for users who follow it or the related entity. Then, unread counts and mark-as-read actions should be supported through field-based and condition-based filtering.

*Slightly more polished version, because apparently APIs now need social lives too:*

I'll provide a list of API requirements for you to review. Please check whether they are feasible and whether any details need to be added or clarified.

The core feature is to support user follow management and notification handling. When a movie is created or published, unread notifications should be generated for the relevant followers. The APIs should also support unread notification statistics and mark-as-read operations based on specific fields and filtering conditions.

### Activity logs task

You need to fix the activity logs for issue and comment operations. Just add an Activity record after the corresponding create, update, and delete APIs.

Also, make sure the corresponding action strings match the test requirements exactly. Because naturally the test will fail over one tiny string mismatch, as software loves being dramatic.

### Frontend / API integration task

Please fix a few features.

Start by checking the API integration and make sure the parameter names are not wrong. For example, fields like `movieId` and `token` need to be consistent with what the backend expects.

After that, update the frontend state logic to properly manage the displayed content and lists. That should be enough once the API fields and state handling are corrected.

### Market API task

Please fix the market-related API business logic issues.

First, align the status checks, data validation, and fund validation across the relevant APIs. Creation, display, and state transitions should all behave as expected, and the request should only proceed when all required checks pass.

Then, follow the test results to identify any remaining issues and make the necessary detail-level fixes.

