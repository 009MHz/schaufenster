# 📘 Test Case ID Naming Convention

> **Quick Start**: Test IDs follow a structured pattern to ensure consistency, traceability, and scalability across thousands of test cases.

---

## 🚀 Quick Reference

### WEB Tests (UI)
```
WEB-<Page>-<Section>-<Number>
```
**Example**: `WEB-DASH-001` → Dashboard test #001

### API Tests
```
<Domain>-<Endpoint>-<Status>-<Serial>-<Country>-<Partner>
```
**Example**: `MOB-LOGIN-200-001` → Mobile login success test
**Example**: `WAP-PAYM-200-001-TH-PERT` → Pertamina payment methods in Thailand

**Country & Partner are optional** – only use when testing country/partner-specific behavior.

---

## 📋 WEB Test IDs

### Pattern
```
WEB-<Page>-<Section>-<Number>
```

### Page Codes (from Sidebar)

| Code | Page | Code | Page |
|------|------|------|------|
| **DASH** | Dashboard | **USER** | User |
| **MANT** | Maintenance | **PRTN** | Partner |
| **FINA** | Finance | **STNG** | Settings |
| **ENGI** | Engineering | **SUPP** | Support |
| **MRKT** | Marketing | **PICK** | Pickup |
| **ESG** | ESG | **INVT** | Inventory |

### Examples

| Test ID | Description |
|---------|-------------|
| `WEB-DASH-001` | Dashboard loads correctly |
| `WEB-MANT-TXN-001` | Maintenance → Transactions list |
| `WEB-FINA-DONATION-001` | Finance → Create donation |
| `WEB-INVT-ASSET-001` | Inventory → Assets page |

### Complex Pages (Dot Notation with 3-digit Serial)
For pages with many features, use dot notation with 3-digit serial numbers:
```
WEB-INVT-ASSET-001.001  (Navigation: breadcrumb)
WEB-INVT-ASSET-001.002  (Navigation: back button)
WEB-INVT-ASSET-002.001  (Table: columns display)
WEB-INVT-ASSET-002.002  (Table: sorting)
WEB-INVT-ASSET-002.003  (Table: filtering)
```

---

## 📋 API Test IDs

### Pattern
```
<Domain>-<Endpoint>-<Status>-<Serial>-<Country>-<Partner>
```

### Domains

| Code | Domain | Usage |
|------|--------|-------|
| **MOB** | Mobile App | APIs consumed by mobile (iOS/Android) |
| **WAP** | Web App | APIs consumed by web applications (myPertamina, AlfaGift) |
| **DAS** | Dashboard | Admin dashboard APIs |
| **BOX** | Box/Device | Device management APIs |
| **INV** | Inventory | Inventory management APIs |

**Important**: MOB and WAP use the same endpoints (`/app/**`) but different client setups (headers, params).

### Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| **200** | OK | Successful GET, PUT, PATCH |
| **201** | Created | Successful POST |
| **400** | Bad Request | Validation errors, missing fields |
| **401** | Unauthorized | Missing/invalid token |
| **404** | Not Found | Resource doesn't exist |
| **500** | Server Error | Internal errors |

### Serial Numbers
Use **3 digits** (001, 002, 003...) for test variations with the same endpoint and status.

```
MOB-LOGIN-400-001  → Missing username
MOB-LOGIN-400-002  → Missing password
MOB-LOGIN-400-003  → Invalid username format
```

### Optional: Country Codes (2 chars)

**When to use**: Testing country-specific behavior (payment methods, regulations, phone formats)

| Code | Country | Code | Country |
|------|---------|------|---------|
| **ID** | Indonesia | **MY** | Malaysia |
| **TH** | Thailand | **PH** | Philippines |
| **SG** | Singapore | **VN** | Vietnam |

**When to skip**: Global features that work the same everywhere (login, token refresh)

**Examples**:
- `MOB-PAYM-200-001-TH` → Payment methods for Thailand
- `MOB-LOGIN-200-001` → Login (works globally, no country code)

### Optional: Partner Codes (4 chars)

**When to use**: Partner-specific features or different partner behavior (WAP domain only)

| Code | Partner | Description |
|------|---------|-------------|
| **PERT** | myPertamina | Oil company partner |
| **ALFA** | AlfaGift | Retail partner |

**When to skip**: Features that work the same across all partners

**Examples**:
- `WAP-OILRWD-200-001-PERT` → Oil rewards (Pertamina only)
- `WAP-LOGIN-200-001` → Login (all partners, no code)

---

## 🎯 Decision Trees

### Should I add a Country Code?

```
Does behavior change by country?
├─ YES → Add country code: MOB-PAYM-200-001-TH
└─ NO → Skip it: MOB-LOGIN-200-001
```

### Should I add a Partner Code?

```
Is this WAP domain?
├─ NO → Skip partner code
└─ YES → Is this partner-specific?
    ├─ YES (unique feature) → Add code: WAP-OILRWD-200-001-PERT
    ├─ YES (different behavior) → Test each: WAP-PAYM-200-001-PERT / ALFA
    └─ NO (works same for all) → Skip code: WAP-LOGIN-200-001
```

---

## 📚 Common Examples

### Mobile App (MOB)

| Test ID | Description |
|---------|-------------|
| `MOB-LOGIN-200-001` | Valid login |
| `MOB-LOGIN-401-001` | Invalid password |
| `MOB-TKN-200-001` | Refresh token success |
| `MOB-PROF-200-001` | Get user profile |
| `MOB-PAYM-200-001-TH` | Payment methods - Thailand |

### Web App (WAP)

| Test ID | Description |
|---------|-------------|
| `WAP-LOGIN-200-001` | Valid login (all partners) |
| `WAP-DONA-200-001` | Donation request |
| `WAP-OILRWD-200-001-PERT` | Oil rewards (Pertamina only) |
| `WAP-GIFT-200-001-ALFA` | Gift cards (AlfaGift only) |
| `WAP-PAYM-200-001-TH-PERT` | Pertamina payments - Thailand |

---

## 🔑 Key Principles

### 1. Keep IDs Stable
Never renumber test IDs when adding new tests. Just increment the serial number.

### 2. Use Optional Components Wisely
- Start simple: `MOB-LOGIN-200-001`
- Add country only when needed: `MOB-LOGIN-200-001-TH`
- Add partner only when needed: `WAP-OILRWD-200-001-PERT`

### 3. Endpoint Abbreviations
Represent **functionality**, not URL path:
- ✅ Good: `LOTP` = Login OTP
- ❌ Avoid: `APPOTP` (based on URL `/app/otp`)

### 4. MOB vs WAP Separation
Keep separate even though they use same endpoints:
- Different headers (device type, app version, browser)
- Different client behavior
- Better debugging and reporting

### 5. Partner Strategy (WAP only)
- **Common features**: Test once without partner code
- **Partner-specific features**: Test per partner with partner code
- **Different behavior**: Test each partner separately

---

## 💡 Tips for New Joiners

### Starting a New Test?

**Step 1**: Determine the domain
- Testing mobile app API? → `MOB-`
- Testing web app API? → `WAP-`
- Testing dashboard UI? → `WEB-DASH-`

**Step 2**: Find the endpoint abbreviation
- Look at similar tests in the same file
- Check the abbreviation registry (ask your team)
- Keep it 3-6 characters, descriptive

**Step 3**: What's the expected status code?
- Success? → `200` or `201`
- Validation error? → `400`
- Auth error? → `401`
- Not found? → `404`

**Step 4**: Check existing test IDs
- Search for similar tests: `MOB-LOGIN-401-`
- Find the highest serial number
- Add 1 to it (use 3 digits)

**Step 5**: Do you need country/partner codes?
- Most of the time? **NO**
- Only add if testing country/partner-specific behavior

### Example Workflow

**Task**: Test invalid password for mobile login

1. Domain: Mobile API → `MOB-`
2. Endpoint: Login → `LOGIN-`
3. Status: Unauthorized → `401-`
4. Search existing: Find `MOB-LOGIN-401-001` exists
5. Use next serial: `MOB-LOGIN-401-002`
6. Country/Partner: Not needed for this test

**Result**: `MOB-LOGIN-401-002`

---

## 📊 Benefits

| Benefit | Description |
|---------|-------------|
| **Clarity** | Easy to understand at a glance |
| **Scalability** | Supports thousands of test cases |
| **Traceability** | Maps to API docs and requirements |
| **No Renumbering** | Add new tests without changing existing IDs |
| **Multi-Country** | Supports international expansion |
| **Multi-Partner** | Supports white-label implementations |
| **Tool-Friendly** | Works with Allure, JIRA, TestRail, etc. |

---

## 🆘 Need Help?

**Can't find existing test IDs?**
```bash
# Search for similar tests
grep -r "MOB-LOGIN" tests/api/
```

**Not sure about endpoint abbreviation?**
- Check similar test files
- Ask your team lead
- Look at the codebase's endpoint naming

**Country/Partner code confusion?**
- Default: Skip it (most tests don't need it)
- Only add if the test is specifically for that country/partner

**Still stuck?**
- Check examples in this doc
- Look at similar existing tests
- Ask your team!

---

## 📝 Summary

### WEB Tests
`WEB-<Page>-<Section>-<Number>` → Simple, follows UI structure

### API Tests
`<Domain>-<Endpoint>-<Status>-<Serial>` → Start here (covers 80% of tests)

Add **optional** components only when needed:
- `-<Country>` → For country-specific tests
- `-<Partner>` → For partner-specific tests (WAP only)

**Remember**: Keep it simple, add complexity only when necessary! 🎯
