#!/usr/bin/env python3
"""Builds the local guide pages (bin days, what's on, school term dates).

Each guide is one entry in GUIDES below: its own copy, FAQs and fun facts,
wrapped in the shared page layout. Run from anywhere:

    python3 scripts/build-guides.py

It writes guides/<slug>/index.html for each guide. To add a guide, add an entry to
GUIDES, run this script, then add the URL to sitemap.xml and llms.txt.
Facts come from slough.gov.uk; re-check them and bump UPDATED when you rebuild.
"""
import html
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FOLDER = "guides"  # every guide lives at /guides/<slug>/
SITE = "https://www.slough.app"
UPDATED_ISO = "2026-11-26"
UPDATED_TEXT = "26 November 2026"

LAYOUT = """<!DOCTYPE html>
<html lang="en-GB">
<head>
  <!-- Built by scripts/build-guides.py. Edit the script, not this file. -->
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-REX65RTK9G"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-REX65RTK9G');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{{DESC}}">
  <meta property="og:title" content="{{OG_TITLE}}" />
  <meta property="og:description" content="{{DESC}}" />
  <meta property="og:type" content="article" />
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="{{URL}}">
  <link rel="icon" type="image/x-icon" href="../../favicon.ico">
  <link rel="stylesheet" href="../../assets/css/shared.min.css?v=2">
  <link rel="stylesheet" href="../../assets/css/site.min.css">
  <link rel="stylesheet" href="../../assets/css/guides.min.css">
  <title>{{TITLE}}</title>
  <meta property="og:url" content="{{URL}}" />
  <meta property="og:site_name" content="Slough App" />
  <meta property="og:image" content="https://www.slough.app/assets/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">
{{JSONLD}}
  </script>
</head>
<body class="nd">

  <a class="skip-link" href="#main">Skip to main content</a>

  <!-- NAV -->
  <nav class="nav nd-nav">
    <div class="nav-inner">
      <a href="/" class="brand" aria-label="Slough App home">
        <img src="../../assets/logo-64.webp" alt="" width="28" height="28">
        <span>Slough App</span>
      </a>
      <div class="nav-links">
        <a href="/">Home</a>
        <a href="/get-slough-app/">Get the App</a>
        <a href="/about/">About</a>
      </div>
      <div class="nav-right">
        <a href="#download" class="nav-cta">Get the app</a>
        <button type="button" class="nav-burger" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </nav>

  <main id="main" tabindex="-1">
  <article class="nd-section guide-section">
    <div class="nd-wrap">
      <p class="guide-crumbs"><a href="/">Home</a> / Slough guides / {{CRUMB}}</p>
      <div class="nd-head guide-head">
        <h1>{{H1}}</h1>
        <p>{{LEDE}}</p>
        <p class="guide-updated">Last checked: <time datetime="{{UPDATED_ISO}}">{{UPDATED_TEXT}}</time></p>
      </div>

      <div class="nd-about-body guide-body">
{{BODY}}

        <h2 id="fun-facts">{{FACTS_HEADING}}</h2>
        <p>{{FACTS_INTRO}}</p>
        <ul class="guide-facts">
{{FACTS}}
        </ul>

        <h2 id="faq">{{FAQ_HEADING}}</h2>
        <div class="nd-faq">
{{FAQS}}
        </div>

        <h2>More Slough guides</h2>
        <ul class="guide-more">
{{MORE}}
        </ul>

        <h2>Sources</h2>
        <p class="guide-sources">{{SOURCES}}</p>
      </div>
    </div>
  </article>

  <section class="nd-download" id="download">
    <div class="nd-wrap">
      <h2>{{CTA_HEADING}}</h2>
      <p>{{CTA_TEXT}}</p>
      <div class="nd-download-row">
        <div class="badges-row">
          <a href="https://apps.apple.com/gb/app/id6760595588" class="store-badge" aria-label="Download on the App Store">
            <svg viewBox="0 0 32 32" fill="currentColor"><path d="M22.154 16.924c-.03-3.072 2.508-4.548 2.622-4.62-1.428-2.088-3.654-2.376-4.446-2.41-1.89-.192-3.69 1.114-4.65 1.114-.96 0-2.442-1.086-4.014-1.056-2.064.03-3.966 1.2-5.028 3.048-2.142 3.72-.546 9.228 1.542 12.246 1.02 1.476 2.238 3.138 3.84 3.078 1.536-.06 2.118-1.002 3.978-1.002 1.86 0 2.382.996 4.014.966 1.662-.03 2.718-1.506 3.732-2.988 1.176-1.716 1.662-3.378 1.692-3.462-.036-.018-3.246-1.248-3.282-4.914z"/><path d="M19.104 7.654c.852-1.032 1.428-2.466 1.272-3.894-1.23.048-2.718.822-3.6 1.854-.792.918-1.482 2.388-1.296 3.798 1.374.108 2.772-.696 3.624-1.758z"/></svg>
            <span class="store-badge-text">
              <span class="store-badge-small">Download on the</span>
              <span class="store-badge-big">App Store</span>
            </span>
          </a>
          <a href="https://play.google.com/store/apps/details?id=com.sloughapp.app" class="store-badge" aria-label="Get it on Google Play">
            <svg viewBox="0 0 32 32"><path d="M4.284 3.456c-.36.384-.564.972-.564 1.716v21.66c0 .744.204 1.332.564 1.716l.09.084L16.5 16.512v-.024L4.374 4.368l-.09.088z" fill="#4285F4"/><path d="M20.544 20.556L16.5 16.512v-.024l4.044-4.044.09.054 4.794 2.724c1.368.78 1.368 2.052 0 2.832l-4.794 2.724-.09-.222z" fill="#FBBC04"/><path d="M20.634 20.778L16.5 16.5 4.284 28.548c.45.48 1.194.54 2.034.06l14.316-7.83" fill="#34A853"/><path d="M20.634 12.222L6.318 4.392c-.84-.48-1.584-.42-2.034.06L16.5 16.5l4.134-4.278z" fill="#EA4335"/></svg>
            <span class="store-badge-text">
              <span class="store-badge-small">Get it on</span>
              <span class="store-badge-big">Google Play</span>
            </span>
          </a>
        </div>
        <div class="nd-qr" aria-label="Scan to download Slough App">
          <img src="../../assets/qr-download.svg" alt="QR code linking to slough.app" width="160" height="160" loading="lazy">
          <span>Scan to download</span>
        </div>
      </div>
    </div>
  </section>

  </main>

  <footer id="about">
    <div class="foot-inner">
      <div class="foot-top">
        <div class="foot-brand">
          <img src="../../assets/logo-64.webp" alt="" width="28" height="28">
          <span>Slough App</span>
        </div>
        <p class="foot-tag">Made for our town.</p>
        <div class="foot-social">
          <a href="https://www.tiktok.com/@sloughapp" rel="me noopener" aria-label="Slough App on TikTok"><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.7 5.7 0 1 0 4.9 5.7V9a7.3 7.3 0 0 0 4.3 1.4V7.3a4.3 4.3 0 0 1-3.2-1.5z"/></svg></a>
          <a href="https://www.instagram.com/sloughapp/" rel="me noopener" aria-label="Slough App on Instagram"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="1" fill="currentColor" stroke="none"/></svg></a>
          <a href="https://www.facebook.com/people/Slough-App/61578994648082/" rel="me noopener" aria-label="Slough App on Facebook"><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.5h2.5l.4-3h-2.9V8.6c0-.9.3-1.5 1.5-1.5h1.5V4.4c-.3 0-1.2-.1-2.2-.1-2.2 0-3.7 1.3-3.7 3.8v2.4H8v3h2.6V21z"/></svg></a>
        </div>
      </div>

      <nav class="foot-links foot-links-row" aria-label="Footer">
        <a href="/">Home</a>
        <a href="/get-slough-app/">Get the App</a>
        <a href="/about/">About</a>
        <a href="/contact/">Help &amp; Contact</a>
        <a href="/child-safety/">Child Safety</a>
        <a href="/terms/">Terms</a>
        <a href="/privacy/">Privacy</a>
        <a href="/accessibility">Accessibility</a>
      </nav>
      <nav class="foot-guides" aria-label="Slough guides">
        <span>Slough guides:</span>
        <a href="/guides/whats-on-in-slough/">What's on</a>
        <a href="/guides/slough-bin-collection-days/">Bin days</a>
        <a href="/guides/slough-school-term-dates/">School term dates</a>
      </nav>
    </div>
    <p class="foot-bottom">&copy; 2026 Slough App. All rights reserved.</p>
  </footer>

{{SCRIPT}}  <script src="../../assets/js/nav.js" defer></script>
</body>
</html>
"""

# --------------------------------------------------------------------------
# 1. BIN COLLECTION DAYS
# --------------------------------------------------------------------------
BINS_BODY = """
        <div class="guide-note">
          <p><strong>The short version</strong></p>
          <ul>
            <li>Grey, red and green bins are each emptied <strong>once every two weeks</strong>, and they are not all collected in the same week.</li>
            <li>Your day and week depend on your road. Look it up in the council's <a href="https://www.slough.gov.uk/directory/30/find-my-bin-day">Find my bin day directory</a>.</li>
            <li>Bins need to be out by <strong>6am</strong> on collection day.</li>
            <li>Christmas and New Year 2026/27 collections move. The <a href="#christmas">revised days are below</a>.</li>
          </ul>
        </div>

        <h2 id="find">How to find your bin day in Slough</h2>
        <p>Slough Borough Council does not publish one calendar for the whole town, because the schedule is set road by road. There are two official ways to check yours.</p>
        <ol>
          <li><strong>The bin day directory.</strong> Open <a href="https://www.slough.gov.uk/directory/30/find-my-bin-day">Find my bin day</a> and search for your road. The result tells you your collection day and which bin goes out in which week.</li>
          <li><strong>The Waste and Recycling Portal.</strong> Sign in at <a href="https://waste.slough.gov.uk/">waste.slough.gov.uk</a> to see your collections, report a missed bin and manage a garden waste subscription.</li>
        </ol>
        <p>The directory search is fussy, so three tips from the council save a failed search:</p>
        <ul>
          <li>Type one keyword from the road name, for example "Bath" for Bath Road.</li>
          <li>Leave out your house number or house name.</li>
          <li>Make sure there is no space after the road name.</li>
        </ul>

        <h2 id="what-goes-where">What goes in each Slough bin</h2>
        <div class="guide-table" tabindex="0" role="region" aria-label="What goes in each Slough bin">
          <table>
            <caption>Slough household bins at a glance</caption>
            <thead>
              <tr><th scope="col">Bin</th><th scope="col">Put in</th><th scope="col">Keep out</th></tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row"><span class="bin-dot bin-grey" aria-hidden="true"></span>Grey bin (rubbish)</th>
                <td>General rubbish, crisp packets, plastic film, polystyrene, disposable nappies, bagged pet waste.</td>
                <td>Food waste, which goes in the silver caddy. Anything that can go in the red bin.</td>
              </tr>
              <tr>
                <th scope="row"><span class="bin-dot bin-red" aria-hidden="true"></span>Red bin (recycling)</th>
                <td>Rinsed drink cans, food tins, glass bottles and jars with their lids, paper, card, plastic bottles, pots and tubs.</td>
                <td>Bin liners, plastic bags, cling film, nappies, polystyrene, takeaway containers, toys, garden or food waste.</td>
              </tr>
              <tr>
                <th scope="row"><span class="bin-dot bin-green" aria-hidden="true"></span>Green bin (garden waste)</th>
                <td>Grass cuttings, leaves, hedge trimmings, small plants and weeds, bark, twigs and small branches.</td>
                <td>Kitchen, food or pet waste, bin liners, glass and plastics.</td>
              </tr>
              <tr>
                <th scope="row"><span class="bin-dot bin-silver" aria-hidden="true"></span>Silver caddy (food waste)</th>
                <td>Food waste. Flats may have a shared communal food bin instead.</td>
                <td>Packaging. See the council's <a href="https://www.slough.gov.uk/bins-waste-recycling/food-waste">food waste page</a> for the full list.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p>A bin filled with the wrong items will not be emptied. The crew leaves a flyer on the handle saying why. Bins weighing more than 30kg are also left, and so are extra bags placed beside the bin.</p>

        <h2 id="christmas">Christmas and New Year 2026/27 bin days</h2>
        <p>Collections scheduled from Monday 21 to Thursday 24 December 2026 happen as normal. From Christmas Day they run late, and they do not catch up until the week of 18 January 2027. The changes cover wheelie bins and food waste.</p>
        <div class="guide-table" tabindex="0" role="region" aria-label="Revised Christmas and New Year bin collection days">
          <table>
            <caption>Revised collection days, Christmas 2026 and New Year 2027</caption>
            <thead>
              <tr><th scope="col">Normal collection day</th><th scope="col">Revised collection day</th></tr>
            </thead>
            <tbody>
              <tr><td>Friday 25 December</td><td>Tuesday 29 December</td></tr>
              <tr><td>Monday 28 December</td><td>Wednesday 30 December</td></tr>
              <tr><td>Tuesday 29 December</td><td>Thursday 31 December</td></tr>
              <tr><td>Wednesday 30 December</td><td>Saturday 2 January</td></tr>
              <tr><td>Thursday 31 December</td><td>Monday 4 January</td></tr>
              <tr><td>Friday 1 January</td><td>Tuesday 5 January</td></tr>
              <tr><td>Monday 4 January</td><td>Wednesday 6 January</td></tr>
              <tr><td>Tuesday 5 January</td><td>Thursday 7 January</td></tr>
              <tr><td>Wednesday 6 January</td><td>Friday 8 January</td></tr>
              <tr><td>Thursday 7 January</td><td>Saturday 9 January</td></tr>
              <tr><td>Friday 8 January</td><td>Monday 11 January</td></tr>
              <tr><td>Monday 11 January</td><td>Tuesday 12 January</td></tr>
              <tr><td>Tuesday 12 January</td><td>Wednesday 13 January</td></tr>
              <tr><td>Wednesday 13 January</td><td>Thursday 14 January</td></tr>
              <tr><td>Thursday 14 January</td><td>Friday 15 January</td></tr>
              <tr><td>Friday 15 January</td><td>Saturday 16 January</td></tr>
            </tbody>
          </table>
        </div>
        <p>The council's own table prints the 31 December row as "31 January", which we have read as a typo. Garden waste is not collected over the two-week Christmas period. Check the <a href="https://www.slough.gov.uk/bins-waste-recycling/bank-holiday-collection-dates">council's bank holiday page</a> for any late changes.</p>

        <h2 id="missed">What to do if your bin is missed</h2>
        <ul>
          <li>Wait until <strong>after 7pm</strong> on your collection day, then report it within <strong>two working days</strong>.</li>
          <li>Report grey, red, green and communal bins through the <a href="https://waste.slough.gov.uk/">Waste and Recycling Portal</a>. Food waste has its own <a href="https://www.slough.gov.uk/xfp/form/206">missed collection form</a>.</li>
          <li>If you have already reported it, do not report it again. Leave the bin out for the next scheduled collection.</li>
        </ul>
        <p>Before reporting, check the handle for a flyer. A bin that was rejected for the wrong contents is not counted as missed.</p>

        <h2 id="costs">Bulky waste, garden waste and new bins: what it costs</h2>
        <div class="guide-table" tabindex="0" role="region" aria-label="Slough waste service charges">
          <table>
            <caption>Charges shown on slough.gov.uk in November 2026</caption>
            <thead>
              <tr><th scope="col">Service</th><th scope="col">Cost</th><th scope="col">Good to know</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">Garden waste subscription</th><td>£55 a year</td><td>25 fortnightly collections. Half price if everyone in the home receives pension credit.</td></tr>
              <tr><th scope="row">Bulky waste collection</th><td>£19 per item, £54 minimum</td><td>Up to 5 items per booking. No changes or refunds once booked.</td></tr>
              <tr><th scope="row">Fridge or freezer collection</th><td>£29.70 each</td><td>Up to 2 per collection.</td></tr>
              <tr><th scope="row">New 180 litre grey bin</th><td>£43</td><td>A 240 litre grey bin is £52, for households of six or more.</td></tr>
              <tr><th scope="row">New 240 litre red bin</th><td>£52</td><td>Up to two red bins are collected per property.</td></tr>
              <tr><th scope="row">New green bin</th><td>£52</td><td>The subscription is charged on top.</td></tr>
            </tbody>
          </table>
        </div>
        <p>Bulky items are collected on your next scheduled rubbish day, so book ahead of it. Details: <a href="https://www.slough.gov.uk/bins-waste-recycling/bulky-waste-collections">bulky waste</a>, <a href="https://www.slough.gov.uk/bins-waste-recycling/garden-waste-collection-service">garden waste</a> and <a href="https://www.slough.gov.uk/bins-waste-recycling/replace-damaged-stolen-missing-bins">replacement bins</a>.</p>

        <h2 id="free-first">Before you pay £54, try giving it away</h2>
        <p>A sofa, wardrobe or bike that still works is often wanted by someone a few streets away. Listing it for free on the Slough App marketplace costs nothing, the person collects it, and it stays out of the waste stream. If nobody takes it within a few days, the council collection is still there.</p>

        <h2 id="tip">Chalvey tip opening hours</h2>
        <p>Chalvey Household Waste Recycling Centre is open seven days a week and takes garden waste free of charge.</p>
        <ul>
          <li><strong>Winter, 1 October to 31 March:</strong> 9am to 5pm.</li>
          <li><strong>Summer, 1 April to 30 September:</strong> 9am to 6pm.</li>
          <li><strong>Christmas Eve and New Year's Eve:</strong> 9am to 1pm.</li>
          <li><strong>Closed:</strong> Christmas Day, Boxing Day and New Year's Day.</li>
        </ul>
        <p>Last entry is 15 minutes before closing, and the site sometimes shuts briefly while containers are swapped. Check the <a href="https://www.slough.gov.uk/household-waste-recycling-centres-waste-transfer-station">council's recycling centre page</a> for access rules before you load the car.</p>
"""

BINS_FACTS = [
    ("The wheelie bin was born in Slough",
     "Frank Rotherham Mouldings, a Slough plastics firm, is widely credited with making the first modern wheelie bin in March 1968. It was built to move waste around the factory floor. Councils only started handing them to households in the 1980s."),
    ("The Trading Estate started out as \"The Dump\"",
     "Slough Trading Estate began as a First World War depot for repairing military vehicles. So many broken lorries piled up there that locals nicknamed it The Dump. It was sold in 1920 and turned into the business estate."),
    ("The first Mars bar was made here",
     "Forrest Mars set up in a rented factory on the Trading Estate, and the first Mars bars were made by hand in Slough in 1932. The wrapper goes in the grey bin."),
]

BINS_FAQS = [
    ("What day is my bin collection in Slough?",
     "It depends on your road. Search for your road name in Slough Borough Council's Find my bin day directory, or sign in to the Waste and Recycling Portal at waste.slough.gov.uk. Leave out your house number when you search."),
    ("How often are bins collected in Slough?",
     "Grey rubbish bins, red recycling bins and green garden waste bins are each collected every two weeks. They are not all collected in the same week, so the directory tells you which bin goes out in which week."),
    ("What time should I put my bin out in Slough?",
     "Bins should be ready for collection by 6am on your collection day."),
    ("Is garden waste collection free in Slough?",
     "No. The green bin is collected by annual subscription only, which costs £55 a year for 25 fortnightly collections. The bin itself costs £52. Chalvey Household Waste Recycling Centre accepts garden waste free of charge."),
    ("How do I report a missed bin in Slough?",
     "Report it after 7pm on your collection day and within two working days, using the council's Waste and Recycling Portal. Missed food waste collections have a separate online form."),
    ("When are bins collected over Christmas 2026 in Slough?",
     "Collections from Monday 21 to Thursday 24 December 2026 are unchanged. From Friday 25 December collections run later than normal, for example Friday 25 December moves to Tuesday 29 December, and the schedule stays shifted until Saturday 16 January 2027."),
]

# --------------------------------------------------------------------------
# 2. WHAT'S ON IN SLOUGH
# --------------------------------------------------------------------------
EVENTS_BODY = """
        <div class="guide-note">
          <p><strong>The short version</strong></p>
          <ul>
            <li>Slough has no single events calendar, so this page maps out <strong>where things happen</strong> and <strong>when in the year</strong> to expect them.</li>
            <li>Small local events, such as school fairs, community meals, sports sessions and group meet-ups, are posted by residents in the <a href="#download">Slough App</a> feed and groups.</li>
            <li>We do not list dates we cannot confirm. Always check with the organiser before you travel.</li>
          </ul>
        </div>

        <h2 id="this-week">Things you can do in Slough any week</h2>
        <ul>
          <li><strong>Skate at Slough Ice Arena.</strong> The rink on Montem Lane runs public sessions and lessons, and hosts ice hockey.</li>
          <li><strong>Run, jog or walk Upton Court parkrun.</strong> A free, timed 5k in Upton Court Park on Saturday mornings.</li>
          <li><strong>Borrow, study or catch a show at The Curve.</strong> The town centre library on William Street also has a performance space and rooms for classes.</li>
          <li><strong>Bowl or bounce at Salt Hill Activity Centre.</strong> Indoor activities including ten-pin bowling, trampolines and soft play, next to Salt Hill Park.</li>
          <li><strong>Watch Slough Town FC.</strong> The Rebels play home games at Arbour Park on Stoke Road.</li>
          <li><strong>Walk Herschel Park.</strong> A restored Victorian park and nature reserve a short walk from the High Street.</li>
        </ul>

        <h2 id="venues">Where events happen in Slough</h2>
        <div class="guide-table" tabindex="0" role="region" aria-label="Slough venues and what they are used for">
          <table>
            <caption>Slough venues and what to look for at each</caption>
            <thead>
              <tr><th scope="col">Venue</th><th scope="col">Area</th><th scope="col">Look for</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">The Curve</th><td>Town centre</td><td>Performances, exhibitions, talks, children's library sessions, adult learning.</td></tr>
              <tr><th scope="row">Upton Court Park</th><td>Upton</td><td>Slough's largest park. Parkrun, funfairs and large outdoor community events.</td></tr>
              <tr><th scope="row">Slough High Street and The Square</th><td>Town centre</td><td>Markets, seasonal entertainment and the Christmas lights switch-on.</td></tr>
              <tr><th scope="row">Slough Ice Arena</th><td>Chalvey</td><td>Public skating, disco sessions, ice hockey fixtures, skating shows.</td></tr>
              <tr><th scope="row">Salt Hill Park and Activity Centre</th><td>Salt Hill</td><td>Family activities indoors, tennis courts and play areas outdoors.</td></tr>
              <tr><th scope="row">Arbour Park</th><td>Stoke Road</td><td>Slough Town FC fixtures and community football.</td></tr>
              <tr><th scope="row">Community centres and places of worship</th><td>Across town</td><td>Festival celebrations, charity meals, classes and youth clubs. These are the events least likely to appear on ticket sites.</td></tr>
            </tbody>
          </table>
        </div>

        <h2 id="year">Slough's year, season by season</h2>
        <p>Dates change every year, and several festivals follow lunar calendars, so treat this as a guide to when to start looking.</p>
        <h3>Spring</h3>
        <p>Vaisakhi in April is marked by Slough's Sikh community. Easter brings school holiday activities at the leisure centres and libraries. Eid celebrations move through the calendar by around eleven days each year, so check the date before planning.</p>
        <h3>Summer</h3>
        <p>The parks do the heavy lifting: funfairs, sports days, community fun days and school summer fairs in June and July. The six-week school holiday is the busiest time for children's activities at The Curve and the leisure centres.</p>
        <h3>Autumn</h3>
        <p>Diwali falls in October or November and lights up homes, temples and restaurants across town. Bonfire Night displays follow in early November, then Remembrance Sunday services.</p>
        <h3>Winter</h3>
        <p>The town centre Christmas lights switch-on has been held in November in recent years, with a stage, market stalls and entertainment on the High Street. December adds school and church carol services, and the ice arena is at its busiest.</p>

        <h2 id="free">Free things to do in Slough</h2>
        <ul>
          <li><strong>The Jubilee River path.</strong> A flat walking and cycling route along the flood relief channel on the southern edge of town, good for spotting herons and kingfishers.</li>
          <li><strong>The Slough Arm of the Grand Union Canal.</strong> A quiet towpath walk that starts near Stoke Road.</li>
          <li><strong>Herschel Park and Upton Court Park.</strong> Open every day, with play areas and plenty of space.</li>
          <li><strong>The Curve.</strong> Free to walk in, with free library membership and regular free sessions for children.</li>
          <li><strong>Meet Station Jim.</strong> The preserved Victorian charity dog stands in a glass case on platform 5 at Slough station.</li>
        </ul>

        <h2 id="nearby">Ten minutes further</h2>
        <p>Slough is well placed for days out. Windsor is six minutes away on the branch line from Slough station to Windsor &amp; Eton Central. Black Park and Langley Park, two country parks run by Buckinghamshire Council, sit just north of Langley. The Elizabeth line runs from Slough into central London without a change.</p>

        <h2 id="how-to-find">How to find out what's on this weekend</h2>
        <ol>
          <li><strong>Open the Slough App feed.</strong> Residents, groups and local organisers post events here first, including the small ones.</li>
          <li><strong>Join a group for your interest.</strong> There are groups across 14 categories, including sport, families, food and faith.</li>
          <li><strong>Check the venue directly.</strong> The Curve, the ice arena and Slough Town FC all publish their own timetables and fixtures.</li>
          <li><strong>Look at ticket sites last.</strong> Their "Slough" pages often include events in Maidenhead, Windsor and London, so check the address.</li>
        </ol>
        <p>Running something yourself? Post it in the app for free so your neighbours see it.</p>
"""

EVENTS_FACTS = [
    ("The world's biggest telescope stood in a Slough garden",
     "William Herschel built a 40-foot telescope behind his house on Windsor Road. It was the largest in the world for 50 years, and with it he discovered two of Saturn's moons, Mimas and Enceladus, in 1789."),
    ("A stuffed dog has watched platform 5 since 1896",
     "Station Jim collected coins for railway widows and orphans in a tin strapped to his harness. When he died in 1896 he was preserved, and he is still at Slough station. He was restored and given a new cabinet in 2025."),
    ("Thunderbirds was filmed on the Trading Estate",
     "Gerry Anderson's puppet studios were on Slough Trading Estate in the 1960s. Thunderbirds, Stingray and Captain Scarlet were all filmed there."),
    ("The Office made Slough a TV landmark",
     "The BBC comedy The Office, first shown in 2001, is set at the Slough branch of the fictional paper company Wernham Hogg."),
]

EVENTS_FAQS = [
    ("What is there to do in Slough this weekend?",
     "Regular options include public skating at Slough Ice Arena, the free Upton Court parkrun on Saturday morning, bowling and trampolines at Salt Hill Activity Centre, events at The Curve and Slough Town FC home games at Arbour Park. For one-off local events, check the Slough App feed and groups, where residents and organisers post what is happening."),
    ("What free things can you do in Slough?",
     "Free options include walking or cycling the Jubilee River path, the towpath of the Slough Arm of the Grand Union Canal, Herschel Park, Upton Court Park, the library at The Curve, and seeing Station Jim, the preserved Victorian charity dog on platform 5 at Slough station."),
    ("Where are events held in Slough?",
     "The main venues are The Curve in the town centre, Upton Court Park for large outdoor events, the High Street for markets and the Christmas lights switch-on, Slough Ice Arena, Salt Hill Park and Arbour Park. Many community events are held in community centres and places of worship."),
    ("When is the Slough Christmas lights switch-on?",
     "It has been held in the town centre in November in recent years. The date changes each year, so check with the organisers or the Slough App feed for the confirmed date."),
    ("What is there to do near Slough?",
     "Windsor is six minutes away by train from Slough station. Black Park and Langley Park country parks are just north of Langley, and the Elizabeth line runs direct from Slough to central London."),
    ("How do I promote a local event in Slough?",
     "You can post your event for free in the Slough App, in the local feed or in a relevant group, so people who live in Slough see it."),
]

# --------------------------------------------------------------------------
# 3. SCHOOL TERM DATES
# --------------------------------------------------------------------------
SCHOOLS_BODY = """
        <div class="guide-note">
          <p><strong>The short version</strong></p>
          <ul>
            <li>These are Slough Borough Council's dates for <strong>community and voluntary controlled schools</strong>.</li>
            <li><strong>Academies, free schools and voluntary aided schools can set their own dates.</strong> Most Slough secondary schools are academies, so check your school's website before you book anything.</li>
            <li>Every school also picks four of its own INSET days, when pupils stay at home.</li>
          </ul>
        </div>
        <p class="guide-note" id="next-break" hidden></p>

        <h2 id="2026-27">Slough school term dates 2026/27</h2>
        <div class="guide-table" tabindex="0" role="region" aria-label="Slough school term dates 2026 to 2027">
          <table>
            <caption>Academic year 2026/27 (195 days)</caption>
            <thead>
              <tr><th scope="col">Term</th><th scope="col">Starts</th><th scope="col">Ends</th><th scope="col">Days</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">Term 1 (autumn)</th><td>Tuesday 1 September 2026</td><td>Friday 23 October 2026</td><td>39</td></tr>
              <tr><th scope="row">Term 2 (autumn)</th><td>Monday 2 November 2026</td><td>Friday 18 December 2026</td><td>35</td></tr>
              <tr><th scope="row">Term 3 (spring)</th><td>Monday 4 January 2027</td><td>Friday 12 February 2027</td><td>30</td></tr>
              <tr><th scope="row">Term 4 (spring)</th><td>Monday 22 February 2027</td><td>Thursday 25 March 2027</td><td>24</td></tr>
              <tr><th scope="row">Term 5 (summer)</th><td>Monday 12 April 2027</td><td>Friday 28 May 2027</td><td>34</td></tr>
              <tr><th scope="row">Term 6 (summer)</th><td>Monday 7 June 2027</td><td>Wednesday 21 July 2027</td><td>33</td></tr>
            </tbody>
          </table>
        </div>
        <p>Tuesday 1 September 2026 was an INSET day set by the council, so pupils at these schools started on Wednesday 2 September at the earliest.</p>

        <h2 id="holidays-2026-27">Slough school holidays 2026/27</h2>
        <div class="guide-table" tabindex="0" role="region" aria-label="Slough school holidays 2026 to 2027">
          <table>
            <caption>Holidays in the 2026/27 school year</caption>
            <thead>
              <tr><th scope="col">Holiday</th><th scope="col">First day off</th><th scope="col">Last day off</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">October half term</th><td>Monday 26 October 2026</td><td>Friday 30 October 2026</td></tr>
              <tr><th scope="row">Christmas</th><td>Monday 21 December 2026</td><td>Friday 1 January 2027</td></tr>
              <tr><th scope="row">February half term</th><td>Monday 15 February 2027</td><td>Friday 19 February 2027</td></tr>
              <tr><th scope="row">Easter</th><td>Friday 26 March 2027</td><td>Friday 9 April 2027</td></tr>
              <tr><th scope="row">May half term</th><td>Monday 31 May 2027</td><td>Friday 4 June 2027</td></tr>
              <tr><th scope="row">Summer</th><td>Thursday 22 July 2027</td><td>Tuesday 31 August 2027</td></tr>
            </tbody>
          </table>
        </div>
        <p>Bank holidays in term time: May Day on Monday 3 May 2027. Good Friday is 26 March and Easter Monday is 29 March 2027, both inside the Easter holiday.</p>

        <h2 id="2027-28">Slough school term dates 2027/28</h2>
        <div class="guide-table" tabindex="0" role="region" aria-label="Slough school term dates 2027 to 2028">
          <table>
            <caption>Academic year 2027/28 (195 days)</caption>
            <thead>
              <tr><th scope="col">Term</th><th scope="col">Starts</th><th scope="col">Ends</th><th scope="col">Days</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">Term 1 (autumn)</th><td>Wednesday 1 September 2027</td><td>Friday 22 October 2027</td><td>38</td></tr>
              <tr><th scope="row">Term 2 (autumn)</th><td>Monday 1 November 2027</td><td>Friday 17 December 2027</td><td>35</td></tr>
              <tr><th scope="row">Term 3 (spring)</th><td>Tuesday 4 January 2028</td><td>Friday 11 February 2028</td><td>29</td></tr>
              <tr><th scope="row">Term 4 (spring)</th><td>Monday 21 February 2028</td><td>Friday 31 March 2028</td><td>30</td></tr>
              <tr><th scope="row">Term 5 (summer)</th><td>Tuesday 18 April 2028</td><td>Friday 26 May 2028</td><td>28</td></tr>
              <tr><th scope="row">Term 6 (summer)</th><td>Monday 5 June 2028</td><td>Friday 21 July 2028</td><td>35</td></tr>
            </tbody>
          </table>
        </div>
        <div class="guide-table" tabindex="0" role="region" aria-label="Slough school holidays 2027 to 2028">
          <table>
            <caption>Holidays in the 2027/28 school year</caption>
            <thead>
              <tr><th scope="col">Holiday</th><th scope="col">First day off</th><th scope="col">Last day off</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">October half term</th><td>Monday 25 October 2027</td><td>Friday 29 October 2027</td></tr>
              <tr><th scope="row">Christmas</th><td>Monday 20 December 2027</td><td>Monday 3 January 2028</td></tr>
              <tr><th scope="row">February half term</th><td>Monday 14 February 2028</td><td>Friday 18 February 2028</td></tr>
              <tr><th scope="row">Easter</th><td>Monday 3 April 2028</td><td>Monday 17 April 2028</td></tr>
              <tr><th scope="row">May half term</th><td>Monday 29 May 2028</td><td>Friday 2 June 2028</td></tr>
            </tbody>
          </table>
        </div>
        <p>Wednesday 1 September 2027 is the council-set INSET day for that year.</p>

        <h2 id="inset">INSET days in Slough</h2>
        <p>Schools have five INSET days a year. The council fixes one, at the very start of September. Each school chooses the other four and tells parents directly, which is why two children at different Slough schools can be off on different days. Look for the list on your school's website or in the first newsletter of the year.</p>

        <h2 id="academies">Why your school's dates might be different</h2>
        <p>The council calendar only binds community and voluntary controlled schools. Academies, free schools and voluntary aided schools set their own, and in Slough that covers a large share of schools, including the grammar schools. Most stay close to the council pattern, but a school can finish a few days earlier in July or move a half term. Three places to check:</p>
        <ul>
          <li>Your school's own term dates page, which is the only source that counts.</li>
          <li>The council's <a href="https://www.slough.gov.uk/schools-slough/school-term-dates">school term dates page</a>, for the community school calendar.</li>
          <li>Other parents. School and year groups in the Slough App are a quick way to confirm an INSET day or an early finish.</li>
        </ul>

        <h2 id="admissions">School admissions deadlines for September 2027</h2>
        <div class="guide-table" tabindex="0" role="region" aria-label="Slough school admissions dates for September 2027 entry">
          <table>
            <caption>Key dates for September 2027 entry</caption>
            <thead>
              <tr><th scope="col">Step</th><th scope="col">Primary (Reception and Year 3)</th><th scope="col">Secondary (Year 7)</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">Application deadline</th><td>15 January 2027</td><td>31 October 2026 (passed). Late applications are open.</td></tr>
              <tr><th scope="row">Offer day</th><td>16 April 2027</td><td>1 March 2027</td></tr>
              <tr><th scope="row">Accept or decline by</th><td>30 April 2027</td><td>14 March 2027</td></tr>
              <tr><th scope="row">Appeals by</th><td>13 May 2027</td><td>26 March 2027</td></tr>
            </tbody>
          </table>
        </div>
        <p>Apply through the council's <a href="https://www.slough.gov.uk/school-admissions/apply-school-place">school admissions pages</a>. Late applications for both phases are accepted until 31 August 2027, but they are considered after on-time ones.</p>
"""

SCHOOLS_FACTS = [
    ("The first zebra crossing was painted in Slough",
     "On 31 October 1951 the world's first zebra crossing was laid out in Slough, after trials by the Road Research Laboratory based in Langley. The road has since been pedestrianised, so the original stripes are gone."),
    ("Slough children sit one 11+ for four schools",
     "Herschel, Langley, Upton Court and St Bernard's Catholic grammar schools share a single entrance test, so a child applying to any of them only sits it once."),
    ("A school named after a planet finder",
     "Herschel Grammar School takes its name from William Herschel, the astronomer who discovered Uranus in 1781 and lived in Slough from 1786 until his death."),
    ("Britain's first salaried woman scientist worked here",
     "Caroline Herschel, William's sister, discovered several comets from Slough. In 1787 King George III began paying her a salary for her astronomy work, a first for a woman in Britain."),
]

SCHOOLS_FAQS = [
    ("When do Slough schools break up for Christmas 2026?",
     "Community and voluntary controlled schools in Slough finish on Friday 18 December 2026 and return on Monday 4 January 2027. Academies, free schools and voluntary aided schools can set different dates."),
    ("When is February half term 2027 in Slough?",
     "February half term runs from Monday 15 February to Friday 19 February 2027. Pupils return on Monday 22 February 2027."),
    ("When are the Easter holidays 2027 in Slough?",
     "Term ends on Thursday 25 March 2027. The Easter holiday runs from Friday 26 March to Friday 9 April 2027, and pupils return on Monday 12 April 2027."),
    ("When is May half term 2027 in Slough?",
     "May half term runs from Monday 31 May to Friday 4 June 2027."),
    ("When do Slough schools break up for summer 2027?",
     "The last day of the summer term is Wednesday 21 July 2027 for community and voluntary controlled schools. The 2027/28 school year starts on Wednesday 1 September 2027, which is an INSET day."),
    ("Do all Slough schools have the same term dates?",
     "No. Slough Borough Council's dates apply to community and voluntary controlled schools. Academies, free schools and voluntary aided schools can set their own term dates, and every school chooses four of its own INSET days, so always check with your school."),
    ("When is the deadline to apply for a primary school place in Slough for September 2027?",
     "The deadline for Reception and Year 3 applications is 15 January 2027. Offers are made on 16 April 2027."),
]

SCHOOLS_SCRIPT = """  <script>
    // Shows the next (or current) school holiday. Dates are the council calendar above.
    (function () {
      var breaks = [
        ['the Christmas holiday', '2026-12-21', '2027-01-01', '2027-01-04'],
        ['February half term', '2027-02-15', '2027-02-19', '2027-02-22'],
        ['the Easter holiday', '2027-03-26', '2027-04-09', '2027-04-12'],
        ['May half term', '2027-05-31', '2027-06-04', '2027-06-07'],
        ['the summer holiday', '2027-07-22', '2027-08-31', '2027-09-01'],
        ['October half term', '2027-10-25', '2027-10-29', '2027-11-01'],
        ['the Christmas holiday', '2027-12-20', '2028-01-03', '2028-01-04'],
        ['February half term', '2028-02-14', '2028-02-18', '2028-02-21'],
        ['the Easter holiday', '2028-04-03', '2028-04-17', '2028-04-18'],
        ['May half term', '2028-05-29', '2028-06-02', '2028-06-05']
      ];
      var el = document.getElementById('next-break');
      if (!el) return;
      var day = function (iso) { var p = iso.split('-'); return new Date(+p[0], p[1] - 1, +p[2]); };
      var fmt = function (d) { return d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }); };
      var now = new Date();
      var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      for (var i = 0; i < breaks.length; i++) {
        var b = breaks[i], start = day(b[1]), end = day(b[2]), back = day(b[3]);
        if (today > end) continue;
        var strong = document.createElement('strong');
        var text;
        if (today >= start) {
          strong.textContent = 'It is ' + b[0] + '. ';
          text = 'Council-calendar schools go back on ' + fmt(back) + '.';
        } else {
          var n = Math.round((start - today) / 86400000);
          strong.textContent = 'Next break: ' + b[0] + ' starts ' + fmt(start) + '. ';
          text = n === 1 ? 'That is tomorrow.' : 'That is ' + n + ' days away.';
        }
        el.appendChild(strong);
        el.appendChild(document.createTextNode(text));
        el.hidden = false;
        return;
      }
    })();
  </script>
"""

GUIDES = [
    {
        "slug": "slough-bin-collection-days",
        "crumb": "Bin collection days",
        "title": "Slough Bin Collection Days 2026/27: Find Your Bin Day | Slough App",
        "og_title": "Slough bin collection days: find your bin day",
        "desc": "Find your Slough bin day, see what goes in the grey, red and green bins, check Christmas 2026 collection changes and what bulky and garden waste cost.",
        "h1": "Slough bin collection days",
        "lede": "How to find your bin day, what goes in which bin, the Christmas 2026 changes and what the extra services cost, all on one page.",
        "body": BINS_BODY,
        "facts_heading": "Slough fun facts: rubbish edition",
        "facts_intro": "Three things about Slough and waste that are worth knowing while you wheel the bin out.",
        "facts": BINS_FACTS,
        "faq_heading": "Slough bin questions",
        "faqs": BINS_FAQS,
        "more_title": "Slough bin collection days",
        "more_blurb": "Find your bin day, what goes where and Christmas changes.",
        "cta_heading": "Never the only one who forgot bin day.",
        "cta_text": "Neighbours on Slough App post reminders, give away furniture for free and flag changes on your street. Free on iOS and Android.",
        "sources": 'Collection rules, charges and revised dates are from <a href="https://www.slough.gov.uk/recycling">Slough Borough Council\'s bins, waste and recycling pages</a>, checked on the date above. Slough App is not run by the council. If anything here differs from slough.gov.uk, the council is right.',
        "script": "",
    },
    {
        "slug": "whats-on-in-slough",
        "crumb": "What's on in Slough",
        "title": "What's On in Slough: Events and Things To Do | Slough App",
        "og_title": "What's on in Slough: events and things to do",
        "desc": "A local's guide to what's on in Slough: where events happen, things to do any week, free ideas, the town's year season by season and how to find this weekend's events.",
        "h1": "What's on in Slough",
        "lede": "Where events happen, what you can do any week of the year, and how to find out what your neighbours are up to this weekend.",
        "body": EVENTS_BODY,
        "facts_heading": "Slough fun facts: showbiz and stargazing",
        "facts_intro": "Four reasons Slough has had more time in the spotlight than people expect.",
        "facts": EVENTS_FACTS,
        "faq_heading": "What's on in Slough: common questions",
        "faqs": EVENTS_FAQS,
        "more_title": "What's on in Slough",
        "more_blurb": "Venues, things to do any week and the town's year.",
        "cta_heading": "See what's on near you.",
        "cta_text": "Local events, groups and meet-ups, posted by people who live here. Slough App is free on iOS and Android.",
        "sources": 'Venue details are from the venues and <a href="https://www.slough.gov.uk/">Slough Borough Council</a>. Opening times, prices and event dates change, so check with the venue or organiser before you set off.',
        "script": "",
    },
    {
        "slug": "slough-school-term-dates",
        "crumb": "School term dates",
        "title": "Slough School Term Dates 2026/27 and 2027/28 | Slough App",
        "og_title": "Slough school term dates and holidays 2026/27 and 2027/28",
        "desc": "Slough school term dates and holidays for 2026/27 and 2027/28, with half terms, INSET days, admissions deadlines and why academy dates can differ.",
        "h1": "Slough school term dates and holidays",
        "lede": "Term dates, half terms and holidays for 2026/27 and 2027/28, plus INSET days, admissions deadlines and the reason your school's calendar might not match.",
        "body": SCHOOLS_BODY,
        "facts_heading": "Slough fun facts: school run edition",
        "facts_intro": "Four facts to try on the walk to school.",
        "facts": SCHOOLS_FACTS,
        "faq_heading": "Slough school holiday questions",
        "faqs": SCHOOLS_FAQS,
        "more_title": "Slough school term dates",
        "more_blurb": "Term dates, half terms and holidays for 2026/27 and 2027/28.",
        "cta_heading": "Ask a parent who knows.",
        "cta_text": "Find other Slough parents, pass on uniform and check that INSET day. Slough App is free on iOS and Android.",
        "sources": 'Term dates are from <a href="https://www.slough.gov.uk/schools-slough/school-term-dates">Slough Borough Council\'s school term dates page</a> and admissions dates from its <a href="https://www.slough.gov.uk/school-admissions">school admissions pages</a>, checked on the date above. Slough App is not run by the council. Your school\'s own published dates always take priority.',
        "script": SCHOOLS_SCRIPT,
    },
]


def esc(text):
    return html.escape(text, quote=True)


def build(guide):
    url = f"{SITE}/{FOLDER}/{guide['slug']}/"
    facts = "\n".join(
        f"          <li><strong>{esc(t)}</strong>{esc(d)}</li>" for t, d in guide["facts"]
    )
    faqs = "\n".join(
        "          <details>\n"
        f"            <summary>{esc(q)}</summary>\n"
        f"            <p>{esc(a)}</p>\n"
        "          </details>"
        for q, a in guide["faqs"]
    )
    more = "\n".join(
        f"          <li><a href=\"/{FOLDER}/{g['slug']}/\">{esc(g['more_title'])}<span>{esc(g['more_blurb'])}</span></a></li>"
        for g in GUIDES
        if g is not guide
    )
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": url + "#article",
                "headline": guide["og_title"],
                "description": guide["desc"],
                "inLanguage": "en-GB",
                "datePublished": "2026-11-26",
                "dateModified": UPDATED_ISO,
                "mainEntityOfPage": url,
                "image": SITE + "/assets/og-image.png",
                "author": {"@type": "Organization", "name": "Slough App", "url": SITE + "/"},
                "publisher": {"@id": SITE + "/#organization"},
                "about": {"@type": "Place", "name": "Slough, Berkshire"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": guide["crumb"], "item": url},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in guide["faqs"]
                ],
            },
        ],
    }
    fields = {
        "TITLE": esc(guide["title"]),
        "OG_TITLE": esc(guide["og_title"]),
        "DESC": esc(guide["desc"]),
        "URL": url,
        "CRUMB": esc(guide["crumb"]),
        "H1": esc(guide["h1"]),
        "LEDE": esc(guide["lede"]),
        "UPDATED_ISO": UPDATED_ISO,
        "UPDATED_TEXT": UPDATED_TEXT,
        "BODY": guide["body"].strip("\n"),
        "FACTS_HEADING": esc(guide["facts_heading"]),
        "FACTS_INTRO": esc(guide["facts_intro"]),
        "FACTS": facts,
        "FAQ_HEADING": esc(guide["faq_heading"]),
        "FAQS": faqs,
        "MORE": more,
        "SOURCES": guide["sources"],
        "CTA_HEADING": esc(guide["cta_heading"]),
        "CTA_TEXT": esc(guide["cta_text"]),
        "JSONLD": json.dumps(jsonld, indent=2, ensure_ascii=False).replace("</", "<\\/"),
        "SCRIPT": guide["script"],
    }
    page = LAYOUT
    for key, value in fields.items():
        page = page.replace("{{" + key + "}}", value)
    out_dir = os.path.join(ROOT, FOLDER, guide["slug"])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("built", FOLDER + "/" + guide["slug"] + "/index.html")


if __name__ == "__main__":
    for g in GUIDES:
        build(g)
