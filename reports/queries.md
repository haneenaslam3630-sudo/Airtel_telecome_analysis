Domain D — Customer Service 

1. Overview Tab

# Card 1 — Total Tickets Raised (January–June 2025, Fixed / Before Filters)

Fixed national baseline before any dashboard filters are applied.

SELECT
    COUNT(*) AS total_tickets
FROM complaints;


Recorded Output (Step 3, G1/G3): 26,841 tickets.

# Card 2 — Step 4 T7 Finding: Open Tickets & Churn Association ("A Link Only")

Computes subscriber counts, churn rates, and the percentage-point gap between subscribers with an open ticket and those without. Display alongside the two-tailed p-value from Step 4 (T7) and the required wording "a link only".

SELECT
    CASE
        WHEN unresolved_count > 0 THEN 'Has open ticket'
        ELSE 'No open ticket'
    END AS open_ticket_status,
    COUNT(*) AS subs,
    SUM(is_churned) AS churned_subs,
    ROUND(100.0 * AVG(is_churned), 2) AS churn_pct
FROM customer_features
GROUP BY open_ticket_status
ORDER BY churn_pct DESC;


Recorded Output (Step 3, J1/J2/J8):

Has open ticket: 6,680 subs | 27.46% churn

No open ticket: 15,320 subs | 22.14% churn

Gap: +5.31 percentage points (associated with higher churn — a link only; add Step 4 T7 two-tailed p-value).

# Card 3 — Open Tickets Count and Percentage of All Tickets

Shows total unresolved tickets and their share of all tickets.

SELECT
    SUM(CASE WHEN is_resolved = 0 THEN 1 ELSE 0 END) AS open_tickets,
    COUNT(*) AS total_tickets,
    ROUND(
        100.0 * SUM(CASE WHEN is_resolved = 0 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
        2
    ) AS pct_open
FROM complaints;


Recorded Output (Step 3, G3): 8,021 open tickets out of 26,841 (29.88%).

Hero Visual — Churn by Complaint History (with Subscriber Counts & Reference Line)

Compares churn across three complaint-history groups (Never complained, All tickets closed, Has open ticket) with subscriber counts and the current-filter churn reference line.

WITH ref AS (
    SELECT
        ROUND(100.0 * AVG(is_churned), 2) AS reference_churn_pct
    FROM customer_features
)
SELECT
    CASE
        WHEN c.complaint_count = 0 THEN '1. Never complained'
        WHEN c.unresolved_count = 0 THEN '2. All tickets closed'
        ELSE '3. Has open ticket'
    END AS complaint_history,
    COUNT(*) AS subs,
    SUM(c.is_churned) AS churned_subs,
    ROUND(100.0 * AVG(c.is_churned), 2) AS churn_pct,
    r.reference_churn_pct
FROM customer_features c
CROSS JOIN ref r
GROUP BY complaint_history, r.reference_churn_pct
ORDER BY complaint_history;


Recorded Output (Step 3, J1 & I1):

1. Never complained: 6,631 subs | 20.03% churn

2. All tickets closed: 8,689 subs | 23.75% churn

3. Has open ticket: 6,680 subs | 27.46% churn

National Reference Line: 23.75%

Supporting Visual 1 — Percentage of Tickets Closed by Complaint Category

Shows ticket closure rate and total ticket count for each of the six complaint categories.

SELECT
    category,
    COUNT(*) AS tickets,
    SUM(CASE WHEN is_resolved = 1 THEN 1 ELSE 0 END) AS closed_tickets,
    ROUND(
        100.0 * SUM(CASE WHEN is_resolved = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
        2
    ) AS pct_closed
FROM complaints
GROUP BY category
ORDER BY pct_closed ASC;


Recorded Output (Step 3, G4):

SIM/KYC: 1,139 tickets | 68.57% closed

Network Coverage: 4,885 tickets | 69.52% closed

Dropped Call: 6,365 tickets | 69.71% closed

Slow Data: 8,035 tickets | 69.97% closed

Billing: 3,738 tickets | 70.87% closed

Recharge Issue: 2,679 tickets | 72.23% closed

Supporting Visual 2 (Bottom / Full Width) — Tickets per 100 Subscribers by Circle

Ranks all 22 circles by complaint intensity (tickets per 100 subscribers), sorted highest first, with subscriber counts.

SELECT
    circle_name,
    region,
    COUNT(*) AS subs,
    SUM(complaint_count) AS total_tickets,
    ROUND(100.0 * SUM(complaint_count) / NULLIF(COUNT(*), 0), 1) AS tickets_per_100_subs
FROM customer_features
GROUP BY circle_name, region
ORDER BY tickets_per_100_subs DESC;


Recorded Output (Step 3, G8 scaled ×100): Top 5 are Tamil Nadu (129.1), Bihar (128.7), Delhi (127.5), Punjab (127.4), and Kolkata (126.9) tickets per 100 subscribers.

2. Category Detail Tab

Parameter Note: Replace 'Slow Data' with your dynamic category parameter (e.g., :selected_category). Both dashboard filters and the category selector narrow the tickets counted.

Selector — Six Complaint Categories (Most Tickets First)

Populates the category selector ordered by ticket volume descending.

SELECT
    category,
    COUNT(*) AS tickets,
    ROUND(100.0 * COUNT(*) / NULLIF((SELECT COUNT(*) FROM complaints), 0), 1) AS pct_of_total
FROM complaints
GROUP BY category
ORDER BY tickets DESC;


Recorded Order (Step 3, G1): Slow Data (8,035 | 29.9%) → Dropped Call (6,365 | 23.7%) → Network Coverage (4,885 | 18.2%) → Billing (3,738 | 13.9%) → Recharge Issue (2,679 | 10.0%) → SIM/KYC (1,139 | 4.2%).

Card 1 — Tickets in Selected Category & Share of All Tickets

Shows ticket count for the selected category and its percentage share of all tickets.

SELECT
    category,
    COUNT(*) AS category_tickets,
    ROUND(
        100.0 * COUNT(*) / NULLIF((SELECT COUNT(*) FROM complaints), 0),
        2
    ) AS pct_of_all_tickets
FROM complaints
WHERE category = 'Slow Data'
GROUP BY category;


Card 2 — Percentage of Tickets Closed & Average Days to Close (Closed Tickets Only)

Calculates closure rate and average resolution days strictly across closed tickets (is_resolved = 1).

SELECT
    category,
    COUNT(*) AS category_tickets,
    ROUND(
        100.0 * SUM(CASE WHEN is_resolved = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
        2
    ) AS pct_closed,
    ROUND(
        AVG(CASE WHEN is_resolved = 1 THEN resolution_days END),
        2
    ) AS avg_days_to_close
FROM complaints
WHERE category = 'Slow Data'
GROUP BY category;


Overall Benchmark (Step 3, G5): 7.54 days average (1.0 min, 14.0 max across 18,820 closed tickets).

Category Benchmark for Slow Data (Step 3, G4): 69.97% closed | 7.55 average days.

Card 3 — Subscribers with an Open Ticket in Selected Category & How Many Left

Deduplicates to unique subscribers (DISTINCT customer_id) so subscribers with multiple open tickets in the same category are counted once.

WITH open_cat_subs AS (
    SELECT DISTINCT customer_id
    FROM complaints
    WHERE category = 'Slow Data'
      AND is_resolved = 0
)
SELECT
    COUNT(*) AS subs_with_open_ticket,
    SUM(c.is_churned) AS subs_who_left,
    ROUND(100.0 * AVG(c.is_churned), 2) AS churn_pct
FROM open_cat_subs o
JOIN customer_features c
  ON c.customer_id = o.customer_id;


Hero Visual — Tickets in Selected Category by Month (January–June 2025)

Tracks monthly ticket volume (and open tickets) for the selected category across the 6-month window.

SELECT
    strftime('%Y-%m', complaint_date) AS month, -- verify date column name in complaints
    COUNT(*) AS tickets,
    SUM(CASE WHEN is_resolved = 0 THEN 1 ELSE 0 END) AS open_tickets
FROM complaints
WHERE category = 'Slow Data'
  AND complaint_date BETWEEN '2025-01-01' AND '2025-06-30'
GROUP BY month
ORDER BY month;


Supporting Visual 1 — Percentage of Tickets Closed by Support Channel (Selected Category)

Breaks down ticket counts and closure rates across support channels (Store, Call Center, Twitter/X, Airtel App) for the selected category.

SELECT
    channel,
    COUNT(*) AS tickets,
    SUM(CASE WHEN is_resolved = 1 THEN 1 ELSE 0 END) AS closed_tickets,
    ROUND(
        100.0 * SUM(CASE WHEN is_resolved = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
        2
    ) AS pct_closed
FROM complaints
WHERE category = 'Slow Data'
GROUP BY channel
ORDER BY tickets DESC;


Overall Benchmark (Step 3, G2): All four channels sit tightly between 69.72% and 70.36% resolved.

Supporting Visual 2 (Bottom) — Churn: All Tickets Closed vs. Open Ticket (Selected Category + National Reference Line)

Compares churn among subscribers whose tickets in the selected category were all closed versus those with at least one still open, alongside the national churn reference line (23.75%).

WITH cat_subs AS (
    SELECT
        x.customer_id,
        CASE
            WHEN SUM(CASE WHEN x.is_resolved = 0 THEN 1 ELSE 0 END) = 0
            THEN 'All tickets closed'
            ELSE 'Has open ticket'
        END AS ticket_status
    FROM complaints x
    WHERE x.category = 'Slow Data'
    GROUP BY x.customer_id
),
national_ref AS (
    SELECT
        ROUND(100.0 * AVG(is_churned), 2) AS national_churn_pct
    FROM customer_features
)
SELECT
    cs.ticket_status,
    COUNT(*) AS subs,
    SUM(c.is_churned) AS churned_subs,
    ROUND(100.0 * AVG(c.is_churned), 2) AS churn_pct,
    n.national_churn_pct
FROM cat_subs cs
JOIN customer_features c
  ON c.customer_id = cs.customer_id
CROSS JOIN national_ref n
GROUP BY cs.ticket_status, n.national_churn_pct
ORDER BY cs.ticket_status;


3. Optional & Deep-Dive Visuals (Category Detail + Step 3 Extra Context)

Optional 1 — Selected Category Tickets & Closure Rate by Region

Supports the optional regional breakdown for the selected category.

SELECT
    c.region,
    COUNT(*) AS tickets,
    COUNT(DISTINCT x.customer_id) AS affected_subs,
    ROUND(
        100.0 * SUM(CASE WHEN x.is_resolved = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
        2
    ) AS pct_closed
FROM complaints x
JOIN customer_features c
  ON c.customer_id = x.customer_id
WHERE x.category = 'Slow Data'
GROUP BY c.region
ORDER BY tickets DESC;


Optional 2 — Selected Category Tickets by Days-to-Close Band

Shows how quickly tickets in the selected category close versus how many remain open.

SELECT
    CASE
        WHEN is_resolved = 0 OR resolution_days IS NULL THEN '4. Still open'
        WHEN resolution_days <= 4 THEN '1. 1-4 days'
        WHEN resolution_days <= 8 THEN '2. 5-8 days'
        ELSE '3. 9-14 days'
    END AS resolution_band,
    COUNT(*) AS tickets,
    ROUND(
        100.0 * COUNT(*) / NULLIF(
            (SELECT COUNT(*) FROM complaints WHERE category = 'Slow Data'),
            0
        ),
        2
    ) AS pct_of_category
FROM complaints
WHERE category = 'Slow Data'
GROUP BY resolution_band
ORDER BY resolution_band;


Optional 3 — Churn by Exact Open Ticket Count (Step 3, J2)

Shows how churn rises monotonically with each additional open ticket.

SELECT
    unresolved_count,
    COUNT(*) AS subs,
    ROUND(100.0 * AVG(is_churned), 2) AS churn_pct
FROM customer_features
GROUP BY unresolved_count
ORDER BY unresolved_count;


Recorded Output (Step 3, J2): 0 open = 22.14% (15,320 subs) | 1 open = 26.07% (5,515 subs) | 2 open = 33.10% (1,018 subs) | 3 open = 37.50% (120 subs).

Reporting Note: Exclude or footnote 4 open (25 subs, 48.00%) and 5 open (2 subs, 100.00%) due to tiny sample sizes.

Optional 4 — Churn by Resolution Speed Band (Step 3, J4)

Demonstrates that resolution speed (1-4 vs 5-8 vs 9-14 days) does not meaningfully separate churn—whether the ticket is closed at all is what aligns with lower churn.

SELECT
    CASE
        WHEN avg_resolution_days IS NULL THEN '4. None closed'
        WHEN avg_resolution_days <= 4 THEN '1. 1-4 days'
        WHEN avg_resolution_days <= 8 THEN '2. 5-8 days'
        ELSE '3. 9-14 days'
    END AS resolution_band,
    COUNT(*) AS subs,
    ROUND(100.0 * AVG(is_churned), 2) AS churn_pct
FROM customer_features
WHERE complaint_count > 0
GROUP BY resolution_band
ORDER BY resolution_band;


Recorded Output (Step 3, J4): 1-4 days: 24.09% (2,810) | 5-8 days: 26.63% (4,495) | 9-14 days: 25.02% (5,248) | None closed: 25.25% (2,816).

Optional 5 — Never Complained vs. Complained Churn (Step 3, G6)

High-level split showing silence is associated with lower churn.

SELECT
    SUM(CASE WHEN complaint_count = 0 THEN 1 ELSE 0 END) AS never_complained,
    SUM(CASE WHEN complaint_count > 0 THEN 1 ELSE 0 END) AS complained,
    ROUND(100.0 * AVG(CASE WHEN complaint_count = 0 THEN is_churned END), 2) AS churn_never_pct,
    ROUND(100.0 * AVG(CASE WHEN complaint_count > 0 THEN is_churned END), 2) AS churn_complained_pct
FROM customer_features;


Recorded Output (Step 3, G6): Never complained = 6,631 subs (20.03% churn) vs. Complained = 15,369 subs (25.36% churn).

Optional 6 — Distribution of Subscribers by Complaint Count (Step 3, G7)

Shows how many subscribers raised 0, 1, 2, ... up to 8 complaints.

SELECT
    complaint_count,
    COUNT(*) AS subs
FROM customer_features
GROUP BY complaint_count
ORDER BY complaint_count;


Recorded Output (Step 3, G7): 0: 6,631 | 1: 7,854 | 2: 4,726 | 3: 1,926 | 4: 625 | 5: 183 | 6: 44 | 7: 10 | 8: 1.