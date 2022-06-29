import { TestBed } from '@angular/core/testing';

import { GetObjectsService } from './get-objects.service';

describe('GetObjectsService', () => {
  let service: GetObjectsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GetObjectsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
