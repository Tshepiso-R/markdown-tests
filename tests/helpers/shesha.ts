import { Page } from '@playwright/test';

/** Wait for the Shesha "Initializing..." spinner to disappear */
export async function waitForShesha(page: Page) {
  const spinner = page.getByText('Initializing');
  await spinner.waitFor({ state: 'visible', timeout: 3_000 }).catch(() => {});
  await spinner.waitFor({ state: 'hidden', timeout: 30_000 }).catch(() => {});
  await page.waitForLoadState('networkidle').catch(() => {});
}

/** Navigate to a URL and wait for Shesha to finish loading */
export async function navigateAndWait(page: Page, path: string) {
  await page.goto(path);
  await waitForShesha(page);
}

/** Wait for a success toast message */
export async function expectSuccess(page: Page, text: string) {
  await page.getByText(text).waitFor({ state: 'visible', timeout: 15_000 });
}

/** Wait for an error toast message */
export async function expectError(page: Page, text: string) {
  await page.getByText(text).waitFor({ state: 'visible', timeout: 15_000 });
}

/** Select an item from an entity picker (ellipsis button → modal → double-click row) */
export async function selectEntityPickerItem(
  page: Page,
  ellipsisButton: string,
  rowText: string
) {
  await page.getByRole('button', { name: ellipsisButton }).click();
  const dialog = page.getByRole('dialog', { name: 'Select Item' });
  await dialog.waitFor({ state: 'visible', timeout: 10_000 });
  await dialog.getByRole('row', { name: new RegExp(rowText) }).dblclick();
  await dialog.waitFor({ state: 'hidden', timeout: 10_000 });
}

/** Type into a Google Places address field and select the first suggestion */
export async function fillGooglePlacesAddress(
  page: Page,
  searchText: string
) {
  const field = page.getByRole('textbox', { name: 'Search places' });
  await field.click();
  await field.pressSequentially(searchText, { delay: 50 });
  await page.waitForTimeout(1500);
  const firstOption = page.getByRole('option').first();
  await firstOption.click();
}
