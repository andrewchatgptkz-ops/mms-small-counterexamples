#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <vector>

namespace {
constexpr int kAgents = 4;
constexpr int kGoods = 11;
using Valuation = std::array<int, kGoods>;
using Profile = std::array<Valuation, kAgents>;

struct MmsResult {
    int value = -1;
    std::array<int, kGoods> labels{};
    std::uint64_t partitions_checked = 0;
};

void EnumeratePartitions(const Valuation& values, int good, int used_bundles,
                         std::array<int, kAgents>& sums,
                         std::array<int, kGoods>& labels,
                         MmsResult& result) {
    if (good == kGoods) {
        if (used_bundles != kAgents) return;
        ++result.partitions_checked;
        const int minimum = *std::min_element(sums.begin(), sums.end());
        if (minimum > result.value) {
            result.value = minimum;
            result.labels = labels;
        }
        return;
    }

    // Prune if too few goods remain to open all missing bundles.
    if (kGoods - good < kAgents - used_bundles) return;

    // Put this good into any already opened bundle.
    for (int bundle = 0; bundle < used_bundles; ++bundle) {
        labels[good] = bundle;
        sums[bundle] += values[good];
        EnumeratePartitions(values, good + 1, used_bundles, sums, labels, result);
        sums[bundle] -= values[good];
    }

    // Or open exactly one new bundle. This restricted-growth convention
    // enumerates every unordered set partition exactly once.
    if (used_bundles < kAgents) {
        labels[good] = used_bundles;
        sums[used_bundles] = values[good];
        EnumeratePartitions(values, good + 1, used_bundles + 1,
                            sums, labels, result);
        sums[used_bundles] = 0;
    }
}

MmsResult ExactMms(const Valuation& values) {
    MmsResult result;
    std::array<int, kAgents> sums{};
    std::array<int, kGoods> labels{};
    EnumeratePartitions(values, 0, 0, sums, labels, result);
    return result;
}

void PrintPartition(const MmsResult& result, const Valuation& values) {
    for (int bundle = 0; bundle < kAgents; ++bundle) {
        int sum = 0;
        std::cout << "  bundle " << (bundle + 1) << ":";
        for (int good = 0; good < kGoods; ++good) {
            if (result.labels[good] == bundle) {
                std::cout << " g" << (good + 1);
                sum += values[good];
            }
        }
        std::cout << "  value=" << sum << '\n';
    }
}
}  // namespace

int main() {
    const Valuation row_type = {7, 12, 11, 8, 6, 16, 21, 9, 1, 28, 1};
    const Valuation column_type = {6, 10, 13, 10, 4, 15, 23, 10, 1, 26, 2};
    const Profile values = {row_type, row_type, column_type, column_type};

    std::array<MmsResult, kAgents> mms;
    std::cout << "Exact MMS calculation by all unordered 4-partitions\n";
    for (int agent = 0; agent < kAgents; ++agent) {
        mms[agent] = ExactMms(values[agent]);
        std::cout << "agent " << (agent + 1)
                  << ": MMS=" << mms[agent].value
                  << ", partitions checked=" << mms[agent].partitions_checked
                  << '\n';
        PrintPartition(mms[agent], values[agent]);
    }

    // A complete allocation is a function from 11 goods to 4 agents.
    // Two bits encode the owner of each good, so the loop has 4^11 iterations.
    const std::uint64_t total_allocations = 1ULL << (2 * kGoods);
    std::uint64_t mms_allocations = 0;
    int best_common_value = std::numeric_limits<int>::min();
    std::uint64_t best_code = 0;
    std::array<int, kAgents> best_utilities{};

    for (std::uint64_t code = 0; code < total_allocations; ++code) {
        std::uint64_t x = code;
        std::array<int, kAgents> utilities{};
        for (int good = 0; good < kGoods; ++good) {
            const int owner = static_cast<int>(x & 3ULL);
            x >>= 2;
            utilities[owner] += values[owner][good];
        }

        bool is_mms = true;
        int minimum = utilities[0];
        for (int agent = 0; agent < kAgents; ++agent) {
            if (utilities[agent] < mms[agent].value) is_mms = false;
            minimum = std::min(minimum, utilities[agent]);
        }
        if (is_mms) ++mms_allocations;
        if (minimum > best_common_value) {
            best_common_value = minimum;
            best_code = code;
            best_utilities = utilities;
        }
    }

    std::cout << "\nComplete-allocation enumeration\n";
    std::cout << "allocations checked=" << total_allocations << " (=4^11)\n";
    std::cout << "MMS allocations=" << mms_allocations << '\n';
    std::cout << "maximum over allocations of min_i v_i(A_i)="
              << best_common_value << '\n';
    std::cout << "one maximizing allocation:\n";

    std::array<std::vector<int>, kAgents> best_bundles;
    std::uint64_t x = best_code;
    for (int good = 0; good < kGoods; ++good) {
        const int owner = static_cast<int>(x & 3ULL);
        x >>= 2;
        best_bundles[owner].push_back(good);
    }
    for (int agent = 0; agent < kAgents; ++agent) {
        std::cout << "  agent " << (agent + 1) << ":";
        for (int good : best_bundles[agent]) std::cout << " g" << (good + 1);
        std::cout << "  value=" << best_utilities[agent] << '\n';
    }

    const std::array<int, kAgents> expected_mms = {30, 30, 30, 30};
    for (int agent = 0; agent < kAgents; ++agent) {
        if (mms[agent].value != expected_mms[agent]) return 2;
        if (mms[agent].partitions_checked != 145750) return 3;
    }
    if (mms_allocations != 0) return 4;
    if (best_common_value != 29) return 5;

    std::cout << "\nVERIFIED: MMS=(30,30,30,30), and no MMS allocation exists.\n";
    return 0;
}
