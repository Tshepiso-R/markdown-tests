import { Page } from '@playwright/test';

/**
 * Select a value from an Ant Design dropdown.
 * Ant Design dropdowns are NOT <select> elements — they are custom divs.
 * Strategy: click the selector trigger, wait for the popup, click the option by title.
 */
export async function selectAntDropdown(
  page: Page,
  comboboxRef: string,
  optionText: string
) {
  await page.locator(comboboxRef).click();
  // Wait for dropdown popup to appear, then click the option by its text content
  const dropdown = page.locator('.ant-select-dropdown:visible');
  await dropdown.waitFor({ state: 'visible', timeout: 10_000 });
  await dropdown
    .locator('.ant-select-item-option')
    .filter({ hasText: new RegExp(`^${optionText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`) })
    .first()
    .click();
}

/**
 * Select from a searchable Ant Design dropdown (e.g. Country fields).
 * Strategy: click to open, type to filter, wait, click the filtered option.
 */
export async function selectSearchableDropdown(
  page: Page,
  comboboxRef: string,
  searchText: string
) {
  await page.locator(comboboxRef).click();
  await page.locator(comboboxRef).fill(searchText);
  await page.waitForTimeout(1000);
  // Wait for dropdown and click the filtered option
  const dropdown = page.locator('.ant-select-dropdown:visible');
  await dropdown.waitFor({ state: 'visible', timeout: 10_000 });
  await dropdown
    .locator('.ant-select-item-option')
    .filter({ hasText: new RegExp(`^${searchText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`) })
    .first()
    .click();
}

/**
 * Click a radio button by its label text within a specific question context.
 */
export async function selectRadio(page: Page, labelText: string, nth: number = 0) {
  await page.getByRole('radio', { name: labelText }).nth(nth).click();
}

/**
 * Click a checkbox. Ant Design checkboxes need click on the wrapper, not the input.
 */
export async function clickCheckbox(page: Page, ref: string) {
  await page.locator(ref).click();
}
