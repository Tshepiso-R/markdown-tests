import { Page } from '@playwright/test';

/**
 * Select a value from an Ant Design dropdown.
 * Ant Design dropdowns are NOT <select> elements — they are custom divs.
 * Strategy: click the selector trigger, wait for the popup, click the option by title.
 */
export async function selectAntDropdown(
  page: Page,
  labelOrRef: string,
  optionText: string
) {
  // Try label-based first (more stable), fall back to ID ref
  if (labelOrRef.startsWith('#')) {
    await page.locator(labelOrRef).click();
  } else {
    // Find the form item by label, then click its .ant-select-selector
    await page.locator('.ant-form-item, .sha-components-container-inner')
      .filter({ hasText: labelOrRef })
      .first()
      .locator('.ant-select-selector')
      .first()
      .click();
  }
  // Wait for option to appear and click it
  await page.getByRole('option', { name: optionText, exact: true })
    .waitFor({ state: 'visible', timeout: 10_000 });
  await page.getByRole('option', { name: optionText, exact: true }).first().click();
}

/**
 * Select from a searchable Ant Design dropdown (e.g. Country fields).
 * Strategy: click to open, type to filter, wait, click the filtered option.
 */
export async function selectSearchableDropdown(
  page: Page,
  labelOrRef: string,
  searchText: string
) {
  // Find the dropdown input by label or ID
  let input;
  if (labelOrRef.startsWith('#')) {
    input = page.locator(labelOrRef);
  } else {
    input = page.locator('.ant-form-item, .sha-components-container-inner')
      .filter({ hasText: labelOrRef })
      .first()
      .locator('.ant-select-selection-search-input')
      .first();
  }
  await input.click();
  await input.fill(searchText);
  await page.waitForTimeout(1000);
  await page.getByRole('option', { name: searchText, exact: true })
    .waitFor({ state: 'visible', timeout: 10_000 });
  await page.getByRole('option', { name: searchText, exact: true }).first().click();
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
