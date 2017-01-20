#include "gtest/include/gtest/gtest.h"
#include "include/solution.h"

using namespace std;

TEST(ArrayEmpty, Empty) {
	Array<int> arr;
	ASSERT_TRUE(arr.empty());
}

TEST(ArrayEmpty, NonEmpty) {
	Array<int> arr;
	arr.push_back(0);
	ASSERT_FALSE(arr.empty());
}

TEST(ArrayEmpty, EmptyAgain) {
	Array<int> arr;
	arr.push_back(1);
	ASSERT_FALSE(arr.empty());
	arr.pop_back();
	ASSERT_TRUE(arr.empty());
}

TEST(ArrayEmpty, Big) {
	Array<unsigned> arr;
	for (unsigned i = 0; i < 10000000; i++) {
		arr.push_back(i);
	}
	ASSERT_FALSE(arr.empty());
	arr.clear();
	ASSERT_TRUE(arr.empty());
}

TEST(ArraySize, Size0) {
	Array<int> arr;
	ASSERT_EQ(arr.size(), 0);
}

TEST(ArraySize, Size3) {
	Array<int> arr;
	arr.push_back(123);
	arr.push_back(456);
	arr.push_back(789);
	ASSERT_EQ(arr.size(), 3);
}

TEST(ArraySize, Size3Again) {
	Array<int> arr;
	arr.push_back(123);
	arr.push_back(456);
	arr.push_back(789);
	arr.push_back(123456789);
	arr.pop_back();
	ASSERT_EQ(arr.size(), 3);
}

TEST(ArraySize, Size10) {
	Array<unsigned> arr;
	for (unsigned i = 0; i < 10; i++) {
		arr.push_back(i);
	}
	ASSERT_EQ(arr.size(), 10);
}

TEST(ArraySize, Big) {
	Array<unsigned> arr;
	for (unsigned i = 0; i < 10000000; i++) {
		arr.push_back(i);
	}
	ASSERT_EQ(arr.size(), 10000000);
	arr.clear();
	ASSERT_EQ(arr.size(), 0);
}

TEST(ArrayAt, Empty1) {
	Array<int> arr;
	ASSERT_THROW(arr.at(0), out_of_range);
}

TEST(ArrayAt, Empty2) {
	Array<int> arr;
	arr.push_back(47);
	arr.pop_back();
	ASSERT_THROW(arr.at(0), out_of_range);
}

TEST(ArrayAt, Empty3) {
	Array<unsigned> arr;
	for (unsigned i = 0; i < 10000000; i++) {
		arr.push_back(i);
	}
	arr.clear();
	ASSERT_THROW(arr.at(0), out_of_range);
}

TEST(ArrayAt, Size5) {
	Array<int> arr;
	arr.push_back(5);
	arr.push_back(31);
	arr.push_back(34);
	arr.push_back(42);
	arr.push_back(47);
	ASSERT_EQ(arr.at(4), 47);
	ASSERT_EQ(arr.at(2), 34);
}

TEST(ArrayAt, Big) {
	Array<int> arr;
	for (unsigned i = 0; i < 10000; i++) {
		arr.push_back(i*i);
	}
	ASSERT_EQ(arr.at(55), 55 * 55);
	ASSERT_EQ(arr.at(9999), 9999 * 9999);
	ASSERT_THROW(arr.at(10000), out_of_range);
}

TEST(ArrayPopBack, Empty1) {
	Array<int> arr;
	ASSERT_THROW(arr.pop_back(), container_empty);
}

TEST(ArrayPopBack, Empty2) {
	Array<int> arr;
	arr.push_back(47);
	arr.pop_back();
	ASSERT_THROW(arr.pop_back(), container_empty);
}

TEST(ArrayPopBack, Empty3) {
	Array<int> arr;
	for (unsigned i = 0; i < 10000000; i++) {
		arr.push_back(i);
	}
	arr.clear();
	ASSERT_THROW(arr.pop_back(), container_empty);
}

TEST(ArrayPopBack, Size5) {
	Array<int> arr;
	arr.push_back(5);
	arr.push_back(31);
	arr.push_back(34);
	arr.push_back(42);
	arr.push_back(47);
	ASSERT_EQ(arr.pop_back(), 47);
	arr.pop_back();
	ASSERT_EQ(arr.pop_back(), 34);
	arr.push_back(58);
	ASSERT_EQ(arr.pop_back(), 58);
	ASSERT_EQ(arr.pop_back(), 31);
}

TEST(ArrayPopBack, Big) {
	Array<int> arr;
	for (unsigned i = 0; i < 10000; i++) {
		arr.push_back(i*i);
	}
	ASSERT_EQ(arr.pop_back(), 9999 * 9999);
	ASSERT_EQ(arr.pop_back(), 9998 * 9998);
	for (unsigned i = 0; i < 10; i++) {
		arr.pop_back();
	}
	ASSERT_EQ(arr.pop_back(), 9987 * 9987);
}
