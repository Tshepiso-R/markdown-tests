import { Page } from '@playwright/test';
import { waitForShesha } from './shesha';

export async function loginAsAdmin(page: Page) {
  await login(page, process.env.ADMIN_USER!, process.env.ADMIN_PASS!);
}

export async function loginAsRM(page: Page) {
  await login(page, process.env.RM_USER!, process.env.RM_PASS!);
}

export async function logout(page: Page) {
  await page.getByText(/System Administrator|Fatima Abrahams/).click();
  await page.getByRole('menuitem', { name: /logout/i }).click();
  await page.waitForURL(/login/);
}

async function login(page: Page, username: string, password: string) {
  await page.goto('/login');
  await page.getByRole('textbox', { name: 'Username' }).waitFor({ state: 'visible', timeout: 30_000 });
  await page.getByRole('textbox', { name: 'Username' }).fill(username);
  await page.getByRole('textbox', { name: 'Password' }).fill(password);
  await page.getByRole('button', { name: 'Sign In' }).click();
  await page.waitForURL(/(?!.*login).*/, { timeout: 30_000 });
  await waitForShesha(page);
}
