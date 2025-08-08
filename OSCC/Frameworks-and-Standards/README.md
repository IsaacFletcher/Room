## Cybersecurity Frameworks and Standards

**Frameworks define a companies security policies and procedures**

### NIST

The National Institute for Standards and Technology Cybersecurity framework is a collection of standards and practices designed to help organizations understand and reduce cybersecurity risks.

**It consists of three main parts: Core, Implementation Tiers and Profiles**

**The Core** is a set of activities and outcomes. It consists of six higher-level functions: Govern, Identify (ID), Protect (PR), Detext (DE), Respond (RS) and Recover (RC)

Each of them have a number of categories.

Identify: Asset Management (ID.AM), Risk Assessment (ID.RA), and Improvement (ID.IM)

Which also have sub-categories in them.

ID.RA has 10 sub-categories: ID.RA.1 (Vulnerabilities in assets are identified, validated, and recorded) through ID.RA.10 (Critical suppliers are assessed prior to acquisition).

These sub-categories go deeper into the possible technical implementations. Go read them if you have time.

**The Implementation Tiers** specify the degree to which an organization's cybersecurity practices satisfy the outcome described by the sub-categories of the **Core**

There are four of these Tiers: partial (the least degree), risk-informed, repeatable, and adaptive.

**The Profiles** refer to the relationship between the present implementation of an oganization's cybersecurity activities (Current Profile) and their desired outcome (Target Profile).

This is determined by the organization's business objectives, requirements, controls, and risk appetite.

 The comparison of these profiles can help the organization perform a gap analysis, as well as understand and prioritize the work required to fill it.

### The ISO/IEC 27000 Family

The Internation Organization for Standardization defines and manages a series of standards applicable across many business sectors. They group these standards into collections known as families or series.

**The ISO 27000** family defines standards for Information Technology (IT) security, cybersecurity and privacy.

**ISO 27001** defines the standards for information security management systems (aka ISMS) to manage risks.

**ISO 27002** focuses on cybersecurity best practices, such as access controls and cryptography.

**ISO 27005** provides guidance on managing risk related to cybersecurity. It suggests that cybersecurity risk can be directly correlated with the potential that threat actors will exploit vulnerabilities in a particylar asset or group of assets, therefore causing harm to an organization.

**ISO 27014** covers the concept of cybersecurity governance, which is to say "by which organizations can evaluate, direct, monitor, and communicate the information security related processes within the organization"

**ISO 27035** addresses incident management, or how organizations should begave when they've detected a security event.

**ISO 27100** among other things, provides a helpful distinction between the concepts of "information security" and "cybersecurity".

Where **ISO 27001** focuses on information and associated risks realated to information, **ISO 27100** pins down cybersecurity as a more general consideration for all risks in cyberspace.

Distinctions like this help make such that we as a community share a common understanding of word so that we can better communicate and coordinate.


## SOC 2

The Assosiation of International Certified Professional Accountants (AICPA) created the system and organization controls (SOC) as a way to audit and report on an organization's security controls.

There are three types of SOC reports known as **SOC 1**, **SOC 2** and **SOC 3**.

> SOC also stands for Security Operations Center. We'll usually refer to SOC audit reports with a number for their type

***SOC 1*** reports focus on financial controls

***SOC 2*** reports focus on security controls, availability, processing integrity, confidentiality, and privacy.

***SOC 3*** reports provide a general summary of SOC 2 reports.


Further the reports are devided based on the duration of the audit.

***Type 1*** report is a point-in-time snapshot.

***Type 2*** report covers several months

SOC audits are not a regulatory or compliance requirement, but many service provider will use a SOC 2 report to demonstrate their cybersecurity standards

SOC audits are not a regulatory or compliance requirement, but many service provider will use a SOC 2 report to demonstrate their cybersecurity standards.

## Security Governance

While frrameworks provide high-level guidance, each organization may implement them in different ways to align with business goals.

Security Governance is the collection of an organizatiion's security policies and procedure.

In other words, frameworks provide a guiding vision, but governance is the practical implication of that vision through policies, procedures, and risk management.


### Policies and Procedures

***Security policies provide high-level guidance for an organization's cybersecurity program.***

These policies define employee and infrastructure expectations.

***Security procedures are the actual implementation of the policies.***

These migh take the form of checklists, such as an employee onboearding checklist.

### Compliance and Regulations

This is the legal part of this whole mess.

**PCI DSS**: So for example an organization that deals with financial transactions has to comply with the PCI DSS (Payment Card Industry Data Security Standard)

This compliance must be assessed annualy

**HIPPA**: A Health Institution has to comply with Health Insurance Portability and Accountability Act (HIPPA) in order to operate in the US as it is a federal law regulating health care coverage and the privace of patient health information.

**GDPR**: GDPR is a law adopted by the Europian Union that regulates data privacy and security. It applies to the private sector and most public sector entities that collect and process personal data. It provides individuals with a wide set of rights over their datam including the well-known "right to be forgotten" and other rights related to notifications of data breaches and portability of data between providers.
