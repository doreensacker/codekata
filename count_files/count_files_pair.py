# Write a Python program the counts the total number of files on your disk
# (start with a specific folder to not wait forever before optimizing)
# - Do not use any Python system lib other than executing a bash command
# - The fastest solution on one reference PC wins!
import os
import uuid
import random
import subprocess
from time import time
import time
import asyncio
import datetime
​
​
class aio_files_on_disk:
    def make_dummy_folder(
        self, current_fol, current_depth=1, max_new_folders=20, max_new_files=20, max_depth=5
    ):
        """
      Use a recursive function to make a folder with a random number of 
      files and sub-folders, where each sub-folder contains a random number 
      files and sub-folders, etc, until max_depth is reached
      """
​
        if current_depth <= max_depth:
            # make files
            num_new_files = random.randint(1, max_new_files)
            for f in range(0, num_new_files):
                uid = uuid.uuid4()
                f = open(os.path.join(current_fol, uid.hex), "a")
                f.close()
​
            # make folders
            new_fols = []
            num_new_fols = random.randint(1, max_new_folders)
            for f in range(0, num_new_fols):
                uid = uuid.uuid4()
                new_fols.append(os.path.join(current_fol, uid.hex))
                os.mkdir(new_fols[-1])
​
            # go through each folder and repeat
            added_files = 0
            added_fols = 0
​
            if current_depth < max_depth:
                for nf in new_fols:
                    dfiles, dfols = self.make_dummy_folder(
                        nf,
                        current_depth=current_depth + 1,
                        max_new_folders=max_new_folders,
                        max_new_files=max_new_files,
                        max_depth=max_depth,
                    )
​
                    added_files += dfiles
                    added_fols += dfols
​
            # return number of files and number of folders
            return added_files + num_new_files, added_fols + num_new_fols
​
    async def run_bash(self, bashcommand, folder):
        return subprocess.check_output(bashcommand, shell=True, cwd=folder)
​
    @asyncio.coroutine
    def async_count_files(self, fol0):
        """
      count the files in fol and all its subfolders, asynchonously
      and using itself as a recursive funtion
      """
​
        # get the files and folders in fol
        # only use bash commands from here on
        bashcommand = "ls  -a -F"
        ls = subprocess.check_output(bashcommand, shell=True, cwd=fol)
        # ls = self.run_bash(bashcommand, fol)
        ls = ls.splitlines()
​
        # only include if not ./ and ../
        ls = [l.decode("utf-8") for l in ls if l.decode("utf-8") not in ["./", "../"]]
​
        # seperate out the folders
        fols = [l for l in ls if l[-1] == "/"]
​
        # number of files
        numfiles = len(ls) - len(fols)
​
        # go through the subfolders and get the number of files in those too
        sub_num_files = 0
        tasks = []
        acount = 0
        for f in fols:
​
            snf = yield from self.async_count_files(os.path.join(fol, f))
            # tasks.append(
            #     asyncio.ensure_future(self.async_count_files(os.path.join(fol, f)))
            # )
​
            # snf = await self.async_count_files(os.path.join(fol, f))
            sub_num_files += snf
​
        # sub_num_files = await asyncio.gather(*tasks)
        # sub_num_files = sum(sub_num_files)
​
        numfiles = numfiles + sub_num_files
​
        return numfiles
​
    def count_files(self, fol):
        """
      count the files in fol and all its subfolders, asynchonously
      and using itself as a recursive funtion
      """
​
        # get the files and folders in fol
        # only use bash commands from here on
        bashcommand = "ls  -a -F"
        ls = subprocess.check_output(bashcommand, shell=True, cwd=fol)
        # ls = self.run_bash(bashcommand, fol)
        ls = ls.splitlines()
​
        # only include if not ./ and ../
        ls = [l.decode("utf-8") for l in ls if l.decode("utf-8") not in ["./", "../"]]
​
        # seperate out the folders
        fols = [l for l in ls if l[-1] == "/"]
​
        # number of files
        numfiles = len(ls) - len(fols)
​
        # go through the subfolders and get the number of files in those too
        sub_num_files = 0
        for f in fols:
            snf = self.count_files(os.path.join(fol, f))
            sub_num_files += snf
​
        numfiles = numfiles + sub_num_files
​
        return numfiles
​
        @asyncio.coroutine
        def countdown(number, n):
            while n > 0:
                print("T-minus", n, "({})".format(number))
                yield from asyncio.sleep(1)
                n -= 1
​
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(countdown("A", 2)), asyncio.ensure_future(countdown("B", 3))]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
​
​
async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")
​
​
async def main():
    await asyncio.gather(count(), count(), count())
​
​
if __name__ == "__main__":
​
    # this works:
    # s = time.perf_counter()
    # asyncio.run(main())
    # elapsed = time.perf_counter() - s
    # print(f"{__file__} executed in {elapsed:0.2f} seconds.")
​
    # # test the function:
    # # create an instance of the aio files on disk class
    # aio_fod = aio_files_on_disk()
​
    # # create a random number of files in a specific folder, we now know how many files we should count
    # dummyfol = "/Users/bensteemers/Documents/data-chapter meeting/20191007/kata/dummyfol"
    # # files_created, fols_created = aio_fod.make_dummy_folder(
    # #     dummyfol, max_depth=3, max_new_folders=20, max_new_files=500
    # # )
    # # print(f"numfiles created = {files_created}, numfols created = {fols_created}")
​
    # # # not async
    # # t1 = time()
    # # files_counted = aio_fod.count_files(dummyfol)
    # # time_passed = time() - t1
    # # print(f"non-async numfiles counted = {files_counted} in {time_passed} seconds")
​
    # async
    t1 = time()
    files_counted = asyncio.run(aio_fod.async_count_files(dummyfol))
    time_passed = time() - t1
    print(f"async numfiles counted = {files_counted} in {time_passed} seconds")