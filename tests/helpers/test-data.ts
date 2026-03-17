/** Generate a unique first name per test run */
export function uniqueFirstName(base: string = 'Ian'): string {
  const suffix = Math.random().toString(36).substring(2, 7);
  return `${base}${suffix}`;
}

export const TEST_CLIENT = {
  title: 'Mr',
  lastName: 'Houvet',
  mobile: '0712345678',
  email: 'promise.raganya@boxfusion.io',
  idNumber: '7708206169188',
  clientType: 'Individual (Individual)',
  province: 'Gauteng',
  preferredComm: 'Email',
  leadChannel: 'Employee Referral',
  classification: 'Development',
  maritalStatus: 'Single',
  country: 'South Africa',
};

export const LOAN_INFO = {
  product: 'R MT Loans',
  businessSummary: 'Farming operations in Gauteng region',
  requestedAmount: '500000',
  existingRelationship: 'None',
  sourcesOfIncome: 'Farming income',
  loanPurpose: 'Purchase Of Livestock',
  loanPurposeAmount: '500000',
};
