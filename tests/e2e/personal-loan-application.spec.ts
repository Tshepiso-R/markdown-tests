import { test, expect, Page } from '@playwright/test';
import { loginAsAdmin, loginAsRM, logout } from '../helpers/auth';
import { selectAntDropdown, selectSearchableDropdown, selectRadio } from '../helpers/ant-design';
import { waitForShesha, navigateAndWait, expectSuccess, selectEntityPickerItem, fillGooglePlacesAddress } from '../helpers/shesha';
import { uniqueFirstName, TEST_CLIENT, LOAN_INFO } from '../helpers/test-data';

test.describe.serial('Personal Loan Application — End to End', () => {
  let page: Page;
  let firstName: string;
  let opportunityUrl: string;

  test.beforeAll(async ({ browser }) => {
    page = await browser.newPage();
    firstName = uniqueFirstName();
  });

  test.afterAll(async () => {
    await page.close();
  });

  // ─── PHASE 1: Lead Capture ───────────────────────────────────────────

  test('TC-01: Create Individual lead', async () => {
    await loginAsAdmin(page);
    await navigateAndWait(page, '/dynamic/LandBank.Crm/LBLead-table');

    // Open "New Lead" dialog
    await page.getByRole('button', { name: /New Lead/ }).click();
    await page.getByRole('dialog', { name: 'Add New Lead' }).waitFor({ state: 'visible', timeout: 10_000 });

    // Fill text fields
    await page.getByRole('textbox').nth(1).fill(firstName);          // First Name
    await page.getByRole('textbox').nth(2).fill(TEST_CLIENT.lastName); // Last Name
    await page.getByRole('textbox').nth(3).fill(TEST_CLIENT.mobile);   // Mobile
    await page.getByRole('textbox').nth(4).fill(TEST_CLIENT.email);    // Email

    // Fill dropdowns (using label-based selectors for stability)
    await selectAntDropdown(page, 'Title', TEST_CLIENT.title);
    await selectAntDropdown(page, 'Client Type', TEST_CLIENT.clientType);
    await selectAntDropdown(page, 'Province', TEST_CLIENT.province);
    await selectAntDropdown(page, 'Preferred Communication', TEST_CLIENT.preferredComm);
    await selectAntDropdown(page, 'Lead Channel', TEST_CLIENT.leadChannel);

    // Submit
    await page.getByRole('button', { name: 'OK' }).click();

    // Assert lead created — appears at top of table
    await page.getByText(firstName).first().waitFor({ state: 'visible', timeout: 10_000 });
    const firstRow = page.getByRole('row').filter({ hasText: firstName }).first();
    await expect(firstRow.getByText('New')).toBeVisible();
  });

  // ─── PHASE 2: Pre-Screening ──────────────────────────────────────────

  test('TC-02: Pre-Screening — all criteria pass', async () => {
    // Open the lead detail
    const leadLink = page.getByRole('row').filter({ hasText: firstName }).first().getByRole('link').first();
    await leadLink.click();
    await waitForShesha(page);

    // Verify lead loaded
    await expect(page.getByText(`Houvet, ${firstName}`)).toBeVisible();
    await expect(page.getByText('New')).toBeVisible();

    // Initiate Pre-Screening
    await page.getByRole('button', { name: /Initiate Pre-Screening/ }).click();
    await page.getByRole('dialog', { name: 'Pre-Screening Assessment' }).waitFor({ state: 'visible', timeout: 10_000 });

    // Answer 7 questions: Q1,2,3,6,7 = Yes (nth 0,1,2,5,6); Q4,5 = No (nth 3,4)
    await page.getByRole('radio', { name: 'Yes' }).nth(0).click(); // Q1: SA citizen
    await page.getByRole('radio', { name: 'Yes' }).nth(1).click(); // Q2: Farming land in SA
    await page.getByRole('radio', { name: 'Yes' }).nth(2).click(); // Q3: Land Bank mandate
    await page.getByRole('radio', { name: 'No' }).nth(3).click();  // Q4: Blacklisted = No
    await page.getByRole('radio', { name: 'No' }).nth(4).click();  // Q5: Debt review = No
    await page.getByRole('radio', { name: 'Yes' }).nth(5).click(); // Q6: Country of residence SA
    await page.getByRole('radio', { name: 'Yes' }).nth(6).click(); // Q7: Access to farming land

    // Tick confirmation checkbox and submit
    await page.getByRole('checkbox').click();
    await page.getByRole('button', { name: /Submit/ }).click();

    // Assert pass
    await expectSuccess(page, 'Pre-assessment passed');
    await expectSuccess(page, 'Opportunity created');

    // Verify lead converted
    await expect(page.getByText('Converted')).toBeVisible();

    // Capture opportunity URL
    const oppLink = page.getByRole('link', { name: new RegExp(`${firstName} Houvet`) }).first();
    await expect(oppLink).toBeVisible();
    opportunityUrl = await oppLink.getAttribute('href') || '';
  });

  // ─── PHASE 3: Opportunity Setup ──────────────────────────────────────

  test('TC-03: Edit Client Info — fill all fields except marital regime', async () => {
    // Switch to RM (Fatima)
    await logout(page);
    await loginAsRM(page);

    // Navigate to opportunity
    await navigateAndWait(page, opportunityUrl);
    await expect(page.getByText('Draft')).toBeVisible();

    // Enter edit mode
    await page.getByRole('button', { name: /Edit/ }).first().click();
    await waitForShesha(page);

    // Set Opportunity Owner
    await selectAntDropdown(page, 'Opportunity Owner', 'Fatima Abrahams');

    // Update Client Name to "Ian" and enter ID Number
    const clientNameField = page.getByRole('textbox').nth(1);
    await clientNameField.clear();
    await clientNameField.fill('Ian');
    await page.getByRole('textbox').first().fill(TEST_CLIENT.idNumber); // Client ID Number

    // Country dropdowns (searchable)
    await selectSearchableDropdown(page, 'Country Of Residence', TEST_CLIENT.country);
    await selectSearchableDropdown(page, 'Citizenship', TEST_CLIENT.country);
    await selectSearchableDropdown(page, 'Country Of Origin', TEST_CLIENT.country);

    // Client Classification
    await selectAntDropdown(page, 'Client Classification', TEST_CLIENT.classification);

    // Residential Address (Google Places)
    await fillGooglePlacesAddress(page, '100 Main Street, Johannesburg');

    // Provincial Office
    await selectAntDropdown(page, 'Provincial Office', 'Provincial Office');

    // Marital Status — set to Single, leave Marital Regime empty
    await selectAntDropdown(page, 'Marital Status', TEST_CLIENT.maritalStatus);

    // Save
    await page.getByRole('button', { name: /Save/ }).click();
    await expectSuccess(page, 'Data saved successfully');

    // Verify saved values
    await expect(page.getByText('Fatima Abrahams')).toBeVisible();
    await expect(page.getByText(TEST_CLIENT.idNumber)).toBeVisible();
  });

  test('TC-04: Fill Loan Info — Product, Amount, Purpose', async () => {
    // Enter edit mode
    await page.getByRole('button', { name: /Edit/ }).first().click();
    await waitForShesha(page);

    // Switch to Loan Info tab
    await page.getByRole('tab', { name: 'Loan Info' }).click();
    await waitForShesha(page);

    // Select Product via entity picker
    await page.getByRole('button', { name: 'ellipsis' }).click();
    const dialog = page.getByRole('dialog', { name: 'Select Item' });
    await dialog.waitFor({ state: 'visible', timeout: 10_000 });
    await dialog.getByRole('row', { name: /R MT Loans/ }).dblclick();
    await dialog.waitFor({ state: 'hidden', timeout: 10_000 });

    // Fill text fields
    await page.locator('textarea').fill(LOAN_INFO.businessSummary);          // Business Summary
    await page.getByRole('textbox').nth(1).fill(LOAN_INFO.requestedAmount);  // Requested Amount

    // Dropdowns
    await selectAntDropdown(page, 'Existing Relationship with Bank', LOAN_INFO.existingRelationship);
    await selectAntDropdown(page, 'Sources Of Income', LOAN_INFO.sourcesOfIncome);
    await page.keyboard.press('Escape');

    // Add Loan Purpose row — Purpose dropdown is in the table header row
    await selectAntDropdown(page, 'Purpose', LOAN_INFO.loanPurpose);
    await page.keyboard.press('Escape');
    await page.getByRole('row', { name: /plus-circle/ }).getByRole('textbox').fill(LOAN_INFO.loanPurposeAmount);
    await page.getByRole('button', { name: 'plus-circle' }).click();

    // Save
    await page.getByRole('button', { name: /Save/ }).click();
    await expectSuccess(page, 'Data saved successfully');

    // Verify amount in header
    await expect(page.getByText('500000')).toBeVisible();
  });

  // ─── PHASE 4: Initiate Loan Application ──────────────────────────────

  test('TC-05: Initiate Loan Application', async () => {
    await page.getByRole('button', { name: /Initiate Loan Application/ }).click();
    await expectSuccess(page, 'Loan Application submitted successfully');

    // Verify status changed
    await expect(page.getByText('Verification In Progress')).toBeVisible();

    // "Initiate Loan Application" button should be gone
    await expect(page.getByRole('button', { name: /Initiate Loan Application/ })).toBeHidden();
  });

  // ─── PHASE 5: Confirm Verification Outcomes ──────────────────────────

  test('TC-06: Confirm Verification Outcomes from Inbox', async () => {
    // Navigate to Inbox
    await navigateAndWait(page, '/dynamic/Shesha.Workflow/workflows-inbox');

    // Find the most recent workflow item (first row with "Confirm verification outcomes")
    const workflowRow = page.getByRole('row').filter({ hasText: 'Confirm verification outcomes' }).first();
    await expect(workflowRow).toBeVisible();
    await workflowRow.getByRole('link').first().click();
    await waitForShesha(page);

    // Verify workflow page loaded
    await expect(page.getByText('Confirm verification outcomes')).toBeVisible();
    await expect(page.getByText('In Progress')).toBeVisible();

    // Click "Finalise Verification Outcomes"
    await page.getByRole('button', { name: 'Finalise Verification Outcomes' }).click();
    await waitForShesha(page);

    // Should auto-redirect to onboarding checklist
    await page.waitForTimeout(3_000);
    await expect(page.getByText('Complete Onboarding Checklist')).toBeVisible({ timeout: 30_000 });
  });

  // ─── PHASE 6: Complete Onboarding Checklist ──────────────────────────

  test('TC-07: Complete Onboarding Checklist and finish workflow', async () => {
    await waitForShesha(page);

    // Select Years Of Farming Experience
    await selectAntDropdown(page, 'Years Of Farming Experience', '4 to 6 Years');
    await page.keyboard.press('Escape');

    // Check all checklist items (checkboxes)
    // Water Use Rights
    await page.getByLabel('', { exact: true }).nth(1).click();
    // Support with water rights (conditional — appears after above)
    await page.waitForTimeout(500);
    await page.getByLabel('', { exact: true }).nth(3).click();
    // Business Plan Development Support
    await page.getByLabel('', { exact: true }).nth(2).click();
    // Equipment and Mechanization
    await page.getByLabel('', { exact: true }).nth(4).click();
    // Tax Clearance
    await page.getByLabel('', { exact: true }).nth(5).click();
    // Access to markets
    await page.locator('div:nth-child(3) > div:nth-child(2) > div > div > div > .ant-form-item > .ant-row > .ant-col.ant-col-16 > .ant-form-item-control-input > .ant-form-item-control-input-content > .ant-checkbox-wrapper > .ant-checkbox > .ant-checkbox-input').first().click();
    // Financial Records
    await page.locator('div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > div > .ant-form-item > .ant-row > .ant-col.ant-col-16 > .ant-form-item-control-input > .ant-form-item-control-input-content > .ant-checkbox-wrapper > .ant-checkbox > .ant-checkbox-input').click();
    // Mentor
    await page.locator('div:nth-child(4) > div > div > div > .ant-form-item > .ant-row > .ant-col.ant-col-16 > .ant-form-item-control-input > .ant-form-item-control-input-content > .ant-checkbox-wrapper > .ant-checkbox > .ant-checkbox-input').first().click();
    // Labor Laws
    await page.locator('div:nth-child(4) > div > div:nth-child(2) > div > .ant-form-item > .ant-row > .ant-col.ant-col-16 > .ant-form-item-control-input > .ant-form-item-control-input-content > .ant-checkbox-wrapper > .ant-checkbox > .ant-checkbox-input').click();

    // Submit
    await page.getByRole('button', { name: 'Submit' }).click();
    await expectSuccess(page, 'Checklist saved successfully');

    // Wait for workflow to complete
    await page.waitForTimeout(5_000);
    await expect(page.getByText('COMPLETED')).toBeVisible({ timeout: 30_000 });
  });

  // ─── VERIFICATION: Final Status ──────────────────────────────────────

  test('TC-08: Verify opportunity status is Complete', async () => {
    await navigateAndWait(page, opportunityUrl);

    await expect(page.getByText('Complete')).toBeVisible();
    await expect(page.getByText('Ian')).toBeVisible();
    await expect(page.getByText('Houvet')).toBeVisible();
    await expect(page.getByText(TEST_CLIENT.idNumber)).toBeVisible();
    await expect(page.getByText('500000')).toBeVisible();
  });
});
