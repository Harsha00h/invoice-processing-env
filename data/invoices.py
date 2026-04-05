"""
Sample invoice, purchase order, and ground truth data for all 3 difficulty tiers.
All data is embedded as Python dicts for Docker portability.
"""

# =============================================================================
# EASY TASKS — Field Extraction
# =============================================================================

EASY_TASKS = [
    {
        "id": "easy_001",
        "invoice_text": """
INVOICE

Acme Office Supplies
123 Business Park Drive, Suite 400
Chicago, IL 60601

Invoice Number: INV-2024-0042
Invoice Date: March 15, 2024
Due Date: April 14, 2024

Bill To:
TechCorp International
456 Innovation Way
San Francisco, CA 94105

+--------------------------------------------------+----------+------------+-------------+
| Description                                      | Quantity | Unit Price | Amount      |
+--------------------------------------------------+----------+------------+-------------+
| Premium Copy Paper (Case, 10 reams)              |       12 |     $45.00 |     $540.00 |
| Ballpoint Pens (Box of 50)                       |        8 |     $12.50 |     $100.00 |
| LaserJet Toner Cartridge (Black)                 |        5 |     $89.50 |     $447.50 |
| Desk Organizer Set                               |        4 |     $40.00 |     $160.00 |
+--------------------------------------------------+----------+------------+-------------+

                                                          Subtotal:       $1,247.50
                                                          Tax (0%):           $0.00
                                                          TOTAL:          $1,247.50

Payment Terms: Net 30
""",
        "ground_truth": {
            "vendor_name": "Acme Office Supplies",
            "invoice_number": "INV-2024-0042",
            "date": "2024-03-15",
            "total_amount": 1247.50,
        },
    },
    {
        "id": "easy_002",
        "invoice_text": """
Global Tech Solutions Ltd.
Innovation Campus, Building 7
2200 Technology Blvd, Austin, TX 78701
Phone: (512) 555-0199 | Email: billing@globaltech.com

                              INVOICE

To: Riverside Manufacturing Co.                Invoice #: GTS-87234
    890 Industrial Parkway                     Date: March 22, 2024
    Detroit, MI 48201                          Terms: Net 45

Description                                Qty     Rate         Total
------------------------------------------------------------------------
Cloud Infrastructure Setup (hours)          40    $175.00     $7,000.00
Database Migration Service                   1  $3,500.00     $3,500.00
Annual Security Audit License                1  $2,200.00     $2,200.00
Technical Support (monthly, x3)              3    $450.00     $1,350.00
------------------------------------------------------------------------
                                              Subtotal:      $14,050.00
                                              Sales Tax (8.25%): $1,159.13
                                              ============================
                                              Total Due:     $15,209.13

Please remit payment to: Global Tech Solutions Ltd.
Account: 4455-6677-8899 | Routing: 021000089
""",
        "ground_truth": {
            "vendor_name": "Global Tech Solutions Ltd.",
            "invoice_number": "GTS-87234",
            "date": "2024-03-22",
            "total_amount": 15209.13,
        },
    },
    {
        "id": "easy_003",
        "invoice_text": """
===========================================
        DataStream Analytics Inc.
        55 Market Street, Floor 12
        New York, NY 10005
===========================================

        TAX INVOICE

Invoice Reference: DS-INV-7891
Issued: 22 April 2024
PO Reference: PO-2024-112

Customer:
  Bright Future Education Group
  1400 Learning Lane
  Boston, MA 02108

Services Rendered:
  1. Student Analytics Platform License (Annual)
     Quantity: 1 | Unit Cost: $18,000.00 ............. $18,000.00
  2. Data Integration Consulting (Days)
     Quantity: 15 | Day Rate: $1,200.00 .............. $18,000.00
  3. Custom Dashboard Development
     Quantity: 1 | Fixed Fee: $7,500.00 ..............  $7,500.00
  4. Staff Training Sessions
     Quantity: 6 | Per Session: $800.00 ..............  $4,800.00

                              -------------------
                              Subtotal: $48,300.00
                              Discount (5%): -$2,415.00
                              -------------------
                              Net Amount: $45,885.00
                              Tax (0%): $0.00
                              -------------------
                              TOTAL DUE: $45,885.00
                              -------------------
""",
        "ground_truth": {
            "vendor_name": "DataStream Analytics Inc.",
            "invoice_number": "DS-INV-7891",
            "date": "2024-04-22",
            "total_amount": 45885.00,
        },
    },
    {
        "id": "easy_004",
        "invoice_text": """
Meridian Logistics Corp
Global Shipping & Freight Solutions
700 Harbor View Road, Long Beach, CA 90802

COMMERCIAL INVOICE

Invoice No.: MLC-2024-03318
Date of Issue: 05/10/2024
Customer PO: CUST-PO-4420

Shipped To:
  Pacific Rim Distributors
  300 Warehouse Blvd
  Seattle, WA 98101

  Item Description                      Units    Price/Unit      Total
  -----------------------------------------------------------------------
  Standard Freight (US Domestic, LTL)      3     $1,850.00    $5,550.00
  Expedited Shipping Surcharge             1       $750.00      $750.00
  Warehouse Storage (per pallet/month)    20        $85.00    $1,700.00
  Customs Documentation Fee                1       $350.00      $350.00
  Cargo Insurance (per shipment)           3       $220.00      $660.00
  -----------------------------------------------------------------------
                                        Subtotal:             $9,010.00
                                        Fuel Surcharge (6%):    $540.60
                                        ===============================
                                        GRAND TOTAL:          $9,550.60

Wire Transfer Details: Meridian Logistics Corp | Acct: 1122334455 | Swift: MRLCUS33
""",
        "ground_truth": {
            "vendor_name": "Meridian Logistics Corp",
            "invoice_number": "MLC-2024-03318",
            "date": "2024-05-10",
            "total_amount": 9550.60,
        },
    },
    {
        "id": "easy_005",
        "invoice_text": """
        ╔══════════════════════════════════════════════╗
        ║       AZURE CLOUD SERVICES                   ║
        ║       One Microsoft Way                      ║
        ║       Redmond, WA 98052                      ║
        ╚══════════════════════════════════════════════╝

        Monthly Service Invoice

        Invoice Number: ACS-INV-2024-56789
        Billing Period: June 1 - June 30, 2024
        Invoice Date: July 1, 2024

        Account: Pinnacle Software Inc.
        Account ID: PSI-ENTERPRISE-042

        Service Usage Summary:
        ─────────────────────────────────────────────────────
        Compute (Virtual Machines)           $4,200.00
        Storage (Blob + Table)               $1,850.00
        Networking (Bandwidth + CDN)         $2,100.00
        AI/ML Services (Inference API)       $3,150.00
        Database (Managed PostgreSQL)        $1,150.00
        ─────────────────────────────────────────────────────
        Subtotal                            $12,450.00
        Enterprise Discount (10%)           -$1,245.00
        ─────────────────────────────────────────────────────
        Total Due                           $11,205.00

        Payment Due: July 31, 2024
        Auto-charge to card ending in 4242
""",
        "ground_truth": {
            "vendor_name": "Azure Cloud Services",
            "invoice_number": "ACS-INV-2024-56789",
            "date": "2024-07-01",
            "total_amount": 11205.00,
        },
    },
]


# =============================================================================
# MEDIUM TASKS — Invoice-PO Matching & Mismatch Detection
# =============================================================================

MEDIUM_TASKS = [
    {
        "id": "medium_001",
        "invoice_text": """
INVOICE from: Northern Steel Fabricators
Invoice #: NSF-4410
Date: 2024-06-15

Line Items:
  1. Steel I-Beams (20ft)          Qty: 50    @ $320.00 ea = $16,000.00
  2. Steel Plates (4x8 ft)         Qty: 30    @ $185.00 ea =  $5,550.00
  3. Welding Rods (Box of 100)     Qty: 10    @  $45.00 ea =    $450.00

Subtotal: $22,000.00
Tax: $0.00
Total: $22,000.00
""",
        "purchase_orders": [
            {
                "po_number": "PO-7001",
                "vendor": "Eastern Metal Works",
                "line_items": [
                    {"description": "Steel I-Beams (20ft)", "quantity": 50, "unit_price": 320.00},
                    {"description": "Aluminum Sheets (4x8 ft)", "quantity": 20, "unit_price": 210.00},
                ],
                "total": 20200.00,
            },
            {
                "po_number": "PO-7002",
                "vendor": "Northern Steel Fabricators",
                "line_items": [
                    {"description": "Steel I-Beams (20ft)", "quantity": 50, "unit_price": 320.00},
                    {"description": "Steel Plates (4x8 ft)", "quantity": 30, "unit_price": 185.00},
                    {"description": "Welding Rods (Box of 100)", "quantity": 10, "unit_price": 45.00},
                ],
                "total": 22000.00,
            },
            {
                "po_number": "PO-7003",
                "vendor": "Northern Steel Fabricators",
                "line_items": [
                    {"description": "Steel I-Beams (15ft)", "quantity": 25, "unit_price": 280.00},
                    {"description": "Steel Plates (4x8 ft)", "quantity": 15, "unit_price": 185.00},
                ],
                "total": 9775.00,
            },
        ],
        "ground_truth": {
            "matching_po": "PO-7002",
            "mismatches": [],
        },
    },
    {
        "id": "medium_002",
        "invoice_text": """
INVOICE
Vendor: Bright Horizon Electrical Supply
Invoice Number: BHE-2024-0553
Date: 2024-07-20

Items:
  - Industrial Circuit Breakers (200A)    Qty: 50   @ $125.00 = $6,250.00
  - Copper Wiring (500ft spools)          Qty: 20   @ $340.00 = $6,800.00
  - LED Panel Lights (2x4 ft)             Qty: 100  @ $78.00  = $7,800.00

Total: $20,850.00
""",
        "purchase_orders": [
            {
                "po_number": "PO-8100",
                "vendor": "Bright Horizon Electrical Supply",
                "line_items": [
                    {"description": "Industrial Circuit Breakers (200A)", "quantity": 45, "unit_price": 125.00},
                    {"description": "Copper Wiring (500ft spools)", "quantity": 20, "unit_price": 340.00},
                    {"description": "LED Panel Lights (2x4 ft)", "quantity": 100, "unit_price": 78.00},
                ],
                "total": 20425.00,
            },
            {
                "po_number": "PO-8101",
                "vendor": "Sunbright Electric Co.",
                "line_items": [
                    {"description": "Circuit Breakers (100A)", "quantity": 60, "unit_price": 95.00},
                    {"description": "Copper Wiring (250ft spools)", "quantity": 40, "unit_price": 180.00},
                ],
                "total": 12900.00,
            },
            {
                "po_number": "PO-8102",
                "vendor": "Bright Horizon Electrical Supply",
                "line_items": [
                    {"description": "Industrial Circuit Breakers (200A)", "quantity": 50, "unit_price": 125.00},
                    {"description": "Copper Wiring (500ft spools)", "quantity": 20, "unit_price": 340.00},
                ],
                "total": 13050.00,
            },
        ],
        "ground_truth": {
            "matching_po": "PO-8100",
            "mismatches": [
                {
                    "field": "quantity",
                    "line_item": "Industrial Circuit Breakers (200A)",
                    "invoice_value": "50",
                    "po_value": "45",
                }
            ],
        },
    },
    {
        "id": "medium_003",
        "invoice_text": """
ProChem Industrial Solutions
Invoice #: PCI-29001
Date: August 5, 2024

Bill To: Greenfield Manufacturing

Line Items:
  1. Industrial Solvent (55-gal drum)    Qty: 8   Unit Price: $425.00   Total: $3,400.00
  2. Epoxy Resin Kit (10L)               Qty: 15  Unit Price: $112.00   Total: $1,680.00
  3. Protective Gloves (Case of 200)     Qty: 6   Unit Price: $89.00    Total: $534.00
  4. Safety Goggles (Box of 50)          Qty: 4   Unit Price: $165.00   Total: $660.00

Subtotal: $6,274.00
Hazmat Handling Fee: $150.00
Total Due: $6,424.00
""",
        "purchase_orders": [
            {
                "po_number": "PO-GF-330",
                "vendor": "ProChem Industrial Solutions",
                "line_items": [
                    {"description": "Industrial Solvent (55-gal drum)", "quantity": 8, "unit_price": 425.00},
                    {"description": "Epoxy Resin Kit (10L)", "quantity": 15, "unit_price": 110.00},
                    {"description": "Protective Gloves (Case of 200)", "quantity": 6, "unit_price": 89.00},
                    {"description": "Safety Goggles (Box of 50)", "quantity": 4, "unit_price": 165.00},
                ],
                "total": 6244.00,
            },
            {
                "po_number": "PO-GF-331",
                "vendor": "ChemSource LLC",
                "line_items": [
                    {"description": "Industrial Solvent (55-gal drum)", "quantity": 10, "unit_price": 410.00},
                    {"description": "Epoxy Resin Kit (5L)", "quantity": 20, "unit_price": 62.00},
                ],
                "total": 5340.00,
            },
        ],
        "ground_truth": {
            "matching_po": "PO-GF-330",
            "mismatches": [
                {
                    "field": "unit_price",
                    "line_item": "Epoxy Resin Kit (10L)",
                    "invoice_value": "112.00",
                    "po_value": "110.00",
                }
            ],
        },
    },
    {
        "id": "medium_004",
        "invoice_text": """
Summit Office Interiors
2500 Commerce Drive, Denver, CO 80203
Invoice No: SOI-2024-1177
Invoice Date: September 12, 2024

Customer: Apex Financial Group

Itemized Charges:
  Ergonomic Desk Chair (Model X500)     x 20     @ $485.00     $9,700.00
  Standing Desk (Electric, 60in)        x 20     @ $725.00    $14,500.00
  Monitor Arm (Dual, Clamp-Mount)       x 40     @ $89.00      $3,560.00
  Cable Management Kit                  x 20     @ $35.00        $700.00
  Filing Cabinet (3-Drawer, Locking)    x 10     @ $310.00     $3,100.00

                                        Subtotal:             $31,560.00
                                        Delivery & Install:    $1,500.00
                                        Total:                $33,060.00
""",
        "purchase_orders": [
            {
                "po_number": "PO-AFG-2240",
                "vendor": "Summit Office Interiors",
                "line_items": [
                    {"description": "Ergonomic Desk Chair (Model X500)", "quantity": 20, "unit_price": 485.00},
                    {"description": "Standing Desk (Electric, 60in)", "quantity": 20, "unit_price": 725.00},
                    {"description": "Monitor Arm (Dual, Clamp-Mount)", "quantity": 40, "unit_price": 89.00},
                    {"description": "Cable Management Kit", "quantity": 20, "unit_price": 35.00},
                ],
                "total": 28460.00,
            },
            {
                "po_number": "PO-AFG-2241",
                "vendor": "Summit Office Interiors",
                "line_items": [
                    {"description": "Filing Cabinet (3-Drawer, Locking)", "quantity": 15, "unit_price": 310.00},
                ],
                "total": 4650.00,
            },
        ],
        "ground_truth": {
            "matching_po": "PO-AFG-2240",
            "mismatches": [
                {
                    "field": "extra_line_item",
                    "line_item": "Filing Cabinet (3-Drawer, Locking)",
                    "invoice_value": "present",
                    "po_value": "not_in_po",
                }
            ],
        },
    },
    {
        "id": "medium_005",
        "invoice_text": """
INVOICE
Vendor: Pacific Fresh Produce Co.
Invoice #: PFP-66201
Date: 2024-10-01

Ship To: Golden Gate Catering Services

Products Delivered:
  Organic Avocados (case of 48)      Qty: 25    @ $52.00 = $1,300.00
  Roma Tomatoes (25lb box)           Qty: 40    @ $28.00 = $1,120.00
  Fresh Basil (2lb bundle)           Qty: 30    @ $15.00 =   $450.00
  Mixed Greens (5lb bag)             Qty: 50    @ $18.00 =   $900.00

Subtotal: $3,770.00
Refrigerated Transport: $250.00
Total: $4,020.00
""",
        "purchase_orders": [
            {
                "po_number": "PO-GGCS-901",
                "vendor": "Pacific Fresh Produce Co.",
                "line_items": [
                    {"description": "Organic Avocados (case of 48)", "quantity": 25, "unit_price": 52.00},
                    {"description": "Roma Tomatoes (25lb box)", "quantity": 35, "unit_price": 28.00},
                    {"description": "Fresh Basil (2lb bundle)", "quantity": 30, "unit_price": 15.00},
                    {"description": "Mixed Greens (5lb bag)", "quantity": 50, "unit_price": 18.00},
                ],
                "total": 3630.00,
            },
            {
                "po_number": "PO-GGCS-902",
                "vendor": "Valley Harvest Farms",
                "line_items": [
                    {"description": "Organic Avocados (case of 48)", "quantity": 30, "unit_price": 48.00},
                    {"description": "Roma Tomatoes (25lb box)", "quantity": 40, "unit_price": 26.00},
                ],
                "total": 2480.00,
            },
        ],
        "ground_truth": {
            "matching_po": "PO-GGCS-901",
            "mismatches": [
                {
                    "field": "quantity",
                    "line_item": "Roma Tomatoes (25lb box)",
                    "invoice_value": "40",
                    "po_value": "35",
                }
            ],
        },
    },
]


# =============================================================================
# HARD TASKS — Partial Deliveries, Currency Conversion, Duplicate Detection
# =============================================================================

HARD_TASKS = [
    {
        "id": "hard_001",
        "invoice_text": """
INVOICE
Vendor: Titan Heavy Machinery GmbH
Invoice #: THM-EU-2024-0815
Date: 2024-08-20
Currency: EUR

Line Items Delivered:
  1. Hydraulic Press (Model HP-3000)     Qty: 2   @ EUR 12,500.00 = EUR 25,000.00
  2. Industrial Conveyor Belt (30m)      Qty: 1   @ EUR 8,200.00  = EUR 8,200.00
  3. Safety Guard Rails (set)            Qty: 4   @ EUR 950.00    = EUR 3,800.00

Total: EUR 37,000.00
""",
        "purchase_orders": [
            {
                "po_number": "PO-MFG-5501",
                "vendor": "Titan Heavy Machinery GmbH",
                "line_items": [
                    {"description": "Hydraulic Press (Model HP-3000)", "quantity": 2, "unit_price": 13500.00},
                    {"description": "Industrial Conveyor Belt (30m)", "quantity": 3, "unit_price": 8856.00},
                    {"description": "Safety Guard Rails (set)", "quantity": 4, "unit_price": 1026.00},
                    {"description": "Pneumatic Drill Set", "quantity": 5, "unit_price": 1620.00},
                    {"description": "Replacement Motor (HP-3000)", "quantity": 2, "unit_price": 4320.00},
                ],
                "total": 65664.00,
                "currency": "USD",
            },
        ],
        "exchange_rates": {"EUR_USD": 1.08},
        "historical_invoices": [],
        "ground_truth": {
            "matching_po": "PO-MFG-5501",
            "converted_total": 39960.00,
            "is_duplicate": False,
            "duplicate_of": None,
            "partial_delivery": True,
            "delivered_lines": [
                "Hydraulic Press (Model HP-3000)",
                "Industrial Conveyor Belt (30m)",
                "Safety Guard Rails (set)",
            ],
            "mismatches": [],
        },
    },
    {
        "id": "hard_002",
        "invoice_text": """
INVOICE
Vendor: Sakura Electronics Co., Ltd.
Invoice #: SEC-JP-88421
Date: 2024-09-10
Currency: JPY

Items:
  1. Precision Sensor Module (Type-A)   Qty: 200  @ JPY 15,000 = JPY 3,000,000
  2. Micro Controller Board (Rev 3)     Qty: 500  @ JPY 8,500  = JPY 4,250,000
  3. LED Display Panel (7-inch)         Qty: 100  @ JPY 22,000 = JPY 2,200,000

Total: JPY 9,450,000
""",
        "purchase_orders": [
            {
                "po_number": "PO-ELEC-4420",
                "vendor": "Sakura Electronics Co., Ltd.",
                "line_items": [
                    {"description": "Precision Sensor Module (Type-A)", "quantity": 200, "unit_price": 100.50},
                    {"description": "Micro Controller Board (Rev 3)", "quantity": 500, "unit_price": 56.95},
                    {"description": "LED Display Panel (7-inch)", "quantity": 100, "unit_price": 147.40},
                ],
                "total": 63465.00,
                "currency": "USD",
            },
        ],
        "exchange_rates": {"JPY_USD": 0.0067},
        "historical_invoices": [
            {
                "invoice_id": "SEC-JP-88400",
                "vendor": "Sakura Electronics Co., Ltd.",
                "date": "2024-08-15",
                "total": 9450000,
                "currency": "JPY",
                "line_items": [
                    "Precision Sensor Module (Type-A) x200",
                    "Micro Controller Board (Rev 3) x500",
                    "LED Display Panel (7-inch) x100",
                ],
            }
        ],
        "ground_truth": {
            "matching_po": "PO-ELEC-4420",
            "converted_total": 63315.00,
            "is_duplicate": True,
            "duplicate_of": "SEC-JP-88400",
            "partial_delivery": False,
            "delivered_lines": [
                "Precision Sensor Module (Type-A)",
                "Micro Controller Board (Rev 3)",
                "LED Display Panel (7-inch)",
            ],
            "mismatches": [],
        },
    },
    {
        "id": "hard_003",
        "invoice_text": """
INVOICE
Vendor: Crown Textiles UK Ltd.
Invoice #: CTX-UK-2024-3310
Date: 2024-10-05
Currency: GBP

Delivered Items:
  1. Premium Cotton Fabric (bolt, 50m)    Qty: 20   @ GBP 180.00 = GBP 3,600.00
  2. Silk Blend Material (bolt, 30m)      Qty: 10   @ GBP 420.00 = GBP 4,200.00

Total: GBP 7,800.00
""",
        "purchase_orders": [
            {
                "po_number": "PO-TEX-9901",
                "vendor": "Crown Textiles UK Ltd.",
                "line_items": [
                    {"description": "Premium Cotton Fabric (bolt, 50m)", "quantity": 20, "unit_price": 228.60},
                    {"description": "Silk Blend Material (bolt, 30m)", "quantity": 10, "unit_price": 533.40},
                    {"description": "Polyester Lining (bolt, 100m)", "quantity": 15, "unit_price": 127.00},
                    {"description": "Thread Assortment Pack", "quantity": 30, "unit_price": 38.10},
                ],
                "total": 12438.00,
                "currency": "USD",
            },
        ],
        "exchange_rates": {"GBP_USD": 1.27},
        "historical_invoices": [],
        "ground_truth": {
            "matching_po": "PO-TEX-9901",
            "converted_total": 9906.00,
            "is_duplicate": False,
            "duplicate_of": None,
            "partial_delivery": True,
            "delivered_lines": [
                "Premium Cotton Fabric (bolt, 50m)",
                "Silk Blend Material (bolt, 30m)",
            ],
            "mismatches": [],
        },
    },
    {
        "id": "hard_004",
        "invoice_text": """
INVOICE
Vendor: Alpine Precision Tools AG
Invoice #: APT-CH-55102
Date: 2024-11-01
Currency: EUR

Items Shipped:
  1. CNC Drill Bit Set (Titanium)     Qty: 10   @ EUR 890.00  = EUR 8,900.00
  2. Calibration Instrument (Model C5) Qty: 3    @ EUR 2,100.00 = EUR 6,300.00
  3. Coolant Fluid (20L canister)      Qty: 25   @ EUR 45.00   = EUR 1,125.00

Total: EUR 16,325.00
""",
        "purchase_orders": [
            {
                "po_number": "PO-TOOL-7780",
                "vendor": "Alpine Precision Tools AG",
                "line_items": [
                    {"description": "CNC Drill Bit Set (Titanium)", "quantity": 10, "unit_price": 961.20},
                    {"description": "Calibration Instrument (Model C5)", "quantity": 5, "unit_price": 2268.00},
                    {"description": "Coolant Fluid (20L canister)", "quantity": 25, "unit_price": 48.60},
                    {"description": "Precision Lathe Attachment", "quantity": 2, "unit_price": 5400.00},
                ],
                "total": 33354.00,
                "currency": "USD",
            },
        ],
        "exchange_rates": {"EUR_USD": 1.08},
        "historical_invoices": [
            {
                "invoice_id": "APT-CH-55090",
                "vendor": "Alpine Precision AG",
                "date": "2024-10-29",
                "total": 16325.00,
                "currency": "EUR",
                "line_items": [
                    "CNC Drill Bit Set (Titanium) x10",
                    "Calibration Instrument (Model C5) x3",
                    "Coolant Fluid (20L canister) x25",
                ],
            }
        ],
        "ground_truth": {
            "matching_po": "PO-TOOL-7780",
            "converted_total": 17631.00,
            "is_duplicate": True,
            "duplicate_of": "APT-CH-55090",
            "partial_delivery": True,
            "delivered_lines": [
                "CNC Drill Bit Set (Titanium)",
                "Calibration Instrument (Model C5)",
                "Coolant Fluid (20L canister)",
            ],
            "mismatches": [
                {
                    "field": "quantity",
                    "line_item": "Calibration Instrument (Model C5)",
                    "invoice_value": "3",
                    "po_value": "5",
                }
            ],
        },
    },
    {
        "id": "hard_005",
        "invoice_text": """
INVOICE
Vendor: Nordic Marine Equipment AS
Invoice #: NME-NO-2024-7745
Date: 2024-11-15
Currency: EUR

Delivered Equipment:
  1. Marine GPS Navigator (Pro)        Qty: 5    @ EUR 3,200.00 = EUR 16,000.00
  2. Underwater Sonar System           Qty: 2    @ EUR 8,500.00 = EUR 17,000.00
  3. Deck Winch (Electric, 5-ton)      Qty: 3    @ EUR 4,100.00 = EUR 12,300.00

Total: EUR 45,300.00
""",
        "purchase_orders": [
            {
                "po_number": "PO-NAV-3300",
                "vendor": "Nordic Marine Equipment AS",
                "line_items": [
                    {"description": "Marine GPS Navigator (Pro)", "quantity": 5, "unit_price": 3456.00},
                    {"description": "Underwater Sonar System", "quantity": 2, "unit_price": 9180.00},
                    {"description": "Deck Winch (Electric, 5-ton)", "quantity": 3, "unit_price": 4428.00},
                    {"description": "Anchor Chain (100m)", "quantity": 4, "unit_price": 2160.00},
                    {"description": "Life Raft (25-person)", "quantity": 6, "unit_price": 3780.00},
                ],
                "total": 67620.00,
                "currency": "USD",
            },
        ],
        "exchange_rates": {"EUR_USD": 1.08},
        "historical_invoices": [
            {
                "invoice_id": "NME-NO-2024-7700",
                "vendor": "Nordic Marine AS",
                "date": "2024-10-20",
                "total": 28000.00,
                "currency": "EUR",
                "line_items": [
                    "Marine GPS Navigator (Pro) x5",
                    "Anchor Chain (100m) x4",
                ],
            }
        ],
        "ground_truth": {
            "matching_po": "PO-NAV-3300",
            "converted_total": 48924.00,
            "is_duplicate": False,
            "duplicate_of": None,
            "partial_delivery": True,
            "delivered_lines": [
                "Marine GPS Navigator (Pro)",
                "Underwater Sonar System",
                "Deck Winch (Electric, 5-ton)",
            ],
            "mismatches": [],
        },
    },
]
