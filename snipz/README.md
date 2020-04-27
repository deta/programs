# Snipz

Snipz hosts snippets at a unique url, that can evolve with PRs.

With Snipz, you can create a code snippet, share the link, and start accepting and incorporating code suggestions as they come in.

You can host your own public or permissioned version of Snipz on [DETA](https://deta.sh/) for free. Snipz can be hosted elsewhere, with slight modifications to the database code.

A reference implementation of Snipz is online [here](https://cclwqvx4995d.deta.dev/). For using your own implementation of Snipz, simply replace the `<snipz_host_url>` in the rest of the examples with your own url.

## Creating a Snippet

Create your code snippet from the Snipz home page.

Give it a name and a 'merge password', then hit 'create'. The 'merge password' holds the keys to your snippets destiny.

## Suggesting Changes

After creation, your snippet is visible for others at a url following the convention:

`<snipz_host_url>.deta.dev/snippets/{snippet_id}`

From this url, others can propose changes to this snippet by editing the text editor on the right and hitting 'propose changes'.

## Viewing and Merging Changes

To merge and view suggested changes, visit a snippets review page, which follows the convention:

`<snipz_host_url>.deta.dev/snippets/{snippet_id}/review`


Navigate using the arrows to the desired change, enter the 'merge password' in the input box, and hit 'merge'.

## Modifying Snipz

Snipz is a big WIP. You can submit PRs here, or you can submit PRs within [Snipz itself](https://cclwqvx4995d.deta.dev/snippets/fptk-6045).