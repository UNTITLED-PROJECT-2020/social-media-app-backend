profile/ gives you all profiles as a viewset
for a specific profile you need to go to profile/pk(of user)
and you can post on profile/ with token in header and data in body to register profile of a user
 


profile/ledger gives all the ledger entries(from viewset)
Post request on it with token in header and {'environment':Key of environment} will delete any previous entry
of that user in the Ledger and make a new entry for that environment and returns 2 types of options of users
normal and random from which user can select the type of matchiong and the match the user wants to do(in the case
it returns only 1 users they both are identical)

For The function scoreAdjust please send the number of the user and 1 for increasing and -1 for
decreasing the score
