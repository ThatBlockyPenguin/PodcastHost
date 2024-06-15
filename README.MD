# PodcastHost

## Instructions

> Note: These instructions are very Work-in-Progress right now, and may not be 100% complete.

If you are reading this, I'm going to assume you already have a GitHub account. If you don't, go create one now.

In theory, all you should have to worry about is `config.yaml` and `episodes`, or whatever you've called your episodes folder in the `config.yaml` file.

The steps for publishing a podcast is relatively simple:
1. Purchase a domain name (or don't, you can use GitHub's provided one)
2. Fork this repository. It's as simple as pressing this big `fork` button near the top of the page, inbetween `watch` and `star`.
3. At the top of the page, go to `settings`, then to `pages` on the left-hand side.
4. Set the `source` to `GitHub Actions`, and enter your domain name into `custom domain`, if you have one.
5. Enable "Enforce HTTPS" if you wish.
6. Follow [this guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) on how to add GitHub pages to your domain name.
7. Press `code` near the top of the page.
8. Upload your podcast files into the `episodes` folder, and fill out `config.yaml` with your info.
9. Press `actions` near the top of the page.
10. On the left-hand side of the page, press "Create Podcast RSS Feed", then press "Run Workflow", and then the green "Run Workflow" button.

That's it! The 10 (hopefully complete) steps to publishing your own podccast on GitHub, completely for free!

Enjoy!