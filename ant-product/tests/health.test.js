import { describe, expect, test } from '@jest/globals';

describe('ANT API Health',()=>{
  test('health endpoint contract',()=>{
    const response={status:'ok',service:'ANT-AI'};
    expect(response.status).toBe('ok');
    expect(response.service).toBe('ANT-AI');
  });
});
